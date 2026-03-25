const { PrismaClient } = require('@prisma/client');
const logger = require('../lib/logger');

const prisma = new PrismaClient();

/**
 * Middleware that validates the API key from the x-api-key header.
 * Attaches the website object to req.website on success.
 */
async function authenticateApiKey(req, res, next) {
  try {
    const apiKey = req.headers['x-api-key'];

    if (!apiKey) {
      return res
        .status(401)
        .json({ error: 'API key is required. Pass it in the x-api-key header.' });
    }

    if (typeof apiKey !== 'string' || apiKey.length < 10) {
      return res.status(401).json({ error: 'Invalid API key format.' });
    }

    const website = await prisma.website.findUnique({
      where: { apiKey },
    });

    if (!website) {
      return res.status(401).json({ error: 'Invalid API key.' });
    }

    if (website.status !== 'active') {
      return res.status(403).json({ error: 'Website account is suspended.' });
    }

    req.website = website;
    next();
  } catch (error) {
    logger.error('Auth middleware error', { error: error.message });
    res.status(500).json({ error: 'Authentication failed.' });
  }
}

/**
 * Check message quota for the current billing period.
 */
async function checkMessageQuota(req, res, next) {
  try {
    const website = req.website;
    const limits = { free: 100, pro: 5000, business: Infinity };
    const limit = limits[website.plan] || 100;

    // Reset counter monthly
    const now = new Date();
    const resetAt = new Date(website.messageResetAt);
    if (
      now.getMonth() !== resetAt.getMonth() ||
      now.getFullYear() !== resetAt.getFullYear()
    ) {
      await prisma.website.update({
        where: { id: website.id },
        data: { messageCount: 0, messageResetAt: now },
      });
      website.messageCount = 0;
    }

    if (website.messageCount >= limit) {
      return res.status(429).json({
        error: 'Message limit reached for your plan.',
        plan: website.plan,
        limit,
        used: website.messageCount,
        upgradeUrl: '/api/billing/plans',
      });
    }

    next();
  } catch (error) {
    logger.error('Quota check error', { error: error.message });
    next();
  }
}

module.exports = { authenticateApiKey, checkMessageQuota };

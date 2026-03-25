const express = require('express');
const crypto = require('crypto');
const { PrismaClient } = require('@prisma/client');
const { authenticateApiKey } = require('../middleware/auth');
const logger = require('../lib/logger');

const router = express.Router();
const prisma = new PrismaClient();

/**
 * POST /api/auth/register
 */
router.post('/register', async (req, res) => {
  try {
    const { name, url, email } = req.body;

    if (!name || !url || !email) {
      return res.status(400).json({ error: 'name, url, and email are required.' });
    }

    if (typeof name !== 'string' || name.length > 100) {
      return res.status(400).json({ error: 'Invalid name.' });
    }

    if (typeof email !== 'string' || !email.includes('@') || email.length > 255) {
      return res.status(400).json({ error: 'Invalid email address.' });
    }

    if (typeof url !== 'string' || url.length > 500) {
      return res.status(400).json({ error: 'Invalid URL.' });
    }

    const existing = await prisma.website.findFirst({ where: { url } });
    if (existing) {
      return res
        .status(409)
        .json({ error: 'A website with this URL is already registered.' });
    }

    const apiKey = `arai_${crypto.randomBytes(32).toString('hex')}`;

    const website = await prisma.website.create({
      data: {
        name: name.trim(),
        url: url.trim(),
        email: email.trim().toLowerCase(),
        apiKey,
        plan: 'free',
        status: 'active',
        analytics: { create: {} },
      },
      include: { analytics: true },
    });

    logger.info('Website registered', { id: website.id, name: website.name });

    res.status(201).json({
      id: website.id,
      name: website.name,
      url: website.url,
      apiKey: website.apiKey,
      plan: website.plan,
    });
  } catch (error) {
    logger.error('Registration error', { error: error.message });
    res.status(500).json({ error: 'Failed to register website.' });
  }
});

/**
 * POST /api/auth/login
 */
router.post('/login', async (req, res) => {
  try {
    const { apiKey } = req.body;

    if (!apiKey || typeof apiKey !== 'string' || apiKey.length < 10 || apiKey.length > 200) {
      return res.status(400).json({ error: 'apiKey is required and must be a valid format.' });
    }

    const website = await prisma.website.findUnique({
      where: { apiKey },
      include: { analytics: true },
    });

    if (!website) {
      return res.status(401).json({ error: 'Invalid API key.' });
    }

    res.json({
      id: website.id,
      name: website.name,
      url: website.url,
      email: website.email,
      plan: website.plan,
      status: website.status,
      settings: JSON.parse(website.settings),
      messageCount: website.messageCount,
      analytics: website.analytics,
    });
  } catch (error) {
    logger.error('Login error', { error: error.message });
    res.status(500).json({ error: 'Login failed.' });
  }
});

/**
 * POST /api/auth/regenerate-key
 */
router.post('/regenerate-key', authenticateApiKey, async (req, res) => {
  try {
    const newApiKey = `arai_${crypto.randomBytes(32).toString('hex')}`;

    await prisma.website.update({
      where: { id: req.website.id },
      data: { apiKey: newApiKey },
    });

    logger.info('API key regenerated', { websiteId: req.website.id });

    res.json({ apiKey: newApiKey });
  } catch (error) {
    logger.error('Key regeneration error', { error: error.message });
    res.status(500).json({ error: 'Failed to regenerate API key.' });
  }
});

/**
 * GET /api/auth/me
 */
router.get('/me', authenticateApiKey, async (req, res) => {
  try {
    const website = await prisma.website.findUnique({
      where: { id: req.website.id },
      include: { analytics: true },
    });

    res.json({
      id: website.id,
      name: website.name,
      url: website.url,
      email: website.email,
      plan: website.plan,
      status: website.status,
      settings: JSON.parse(website.settings),
      messageCount: website.messageCount,
      createdAt: website.createdAt,
    });
  } catch (error) {
    logger.error('Get profile error', { error: error.message });
    res.status(500).json({ error: 'Failed to get profile.' });
  }
});

/**
 * PUT /api/auth/settings
 */
router.put('/settings', authenticateApiKey, async (req, res) => {
  try {
    const { primaryColor, position, greeting } = req.body;
    const currentSettings = JSON.parse(req.website.settings);

    // Validate color
    if (primaryColor && !/^#[0-9A-Fa-f]{6}$/.test(primaryColor)) {
      return res.status(400).json({ error: 'Invalid color format. Use hex like #3B82F6.' });
    }

    // Validate position
    if (position && !['bottom-right', 'bottom-left'].includes(position)) {
      return res.status(400).json({ error: 'Position must be bottom-right or bottom-left.' });
    }

    // Validate greeting
    if (greeting && (typeof greeting !== 'string' || greeting.length > 200)) {
      return res.status(400).json({ error: 'Greeting must be under 200 characters.' });
    }

    const updatedSettings = {
      ...currentSettings,
      ...(primaryColor && { primaryColor }),
      ...(position && { position }),
      ...(greeting !== undefined && { greeting }),
    };

    await prisma.website.update({
      where: { id: req.website.id },
      data: { settings: JSON.stringify(updatedSettings) },
    });

    res.json({ settings: updatedSettings });
  } catch (error) {
    logger.error('Settings update error', { error: error.message });
    res.status(500).json({ error: 'Failed to update settings.' });
  }
});

module.exports = router;

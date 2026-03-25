const express = require('express');
const rateLimit = require('express-rate-limit');
const { PrismaClient } = require('@prisma/client');
const { generateResponse } = require('../services/ai');
const logger = require('../lib/logger');

const router = express.Router();
const prisma = new PrismaClient();

const widgetLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 20,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many messages. Please slow down.' },
});

/**
 * POST /api/widget/init
 */
router.post('/init', async (req, res) => {
  try {
    const { apiKey } = req.body;

    if (!apiKey || typeof apiKey !== 'string' || apiKey.length < 10 || apiKey.length > 200) {
      return res.status(400).json({ error: 'apiKey is required and must be a valid key.' });
    }

    const website = await prisma.website.findUnique({
      where: { apiKey },
    });

    if (!website || website.status !== 'active') {
      return res.status(403).json({ error: 'Invalid or inactive widget.' });
    }

    const conversation = await prisma.conversation.create({
      data: {
        websiteId: website.id,
        sessionId: `sess_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        metadata: JSON.stringify({
          userAgent: req.get('User-Agent') || '',
          ip: req.ip,
          referer: req.get('Referer') || '',
        }),
      },
    });

    const settings = JSON.parse(website.settings);

    res.json({
      conversationId: conversation.id,
      settings: {
        primaryColor: settings.primaryColor || '#3B82F6',
        position: settings.position || 'bottom-right',
        greeting: settings.greeting || 'Hi! How can I help you today?',
        name: website.name,
      },
    });
  } catch (error) {
    logger.error('Widget init error', { error: error.message });
    res.status(500).json({ error: 'Failed to initialize widget.' });
  }
});

/**
 * POST /api/widget/chat
 */
router.post('/chat', widgetLimiter, async (req, res) => {
  try {
    const { conversationId, message, apiKey } = req.body;

    if (!conversationId || !message || !apiKey) {
      return res
        .status(400)
        .json({ error: 'conversationId, message, and apiKey are required.' });
    }

    if (typeof conversationId !== 'string' || conversationId.length > 100) {
      return res.status(400).json({ error: 'Invalid conversationId.' });
    }

    if (typeof message !== 'string' || message.length === 0 || message.length > 2000) {
      return res.status(400).json({ error: 'Message must be between 1 and 2000 characters.' });
    }

    if (typeof apiKey !== 'string' || apiKey.length < 10 || apiKey.length > 200) {
      return res.status(400).json({ error: 'Invalid apiKey format.' });
    }

    const website = await prisma.website.findUnique({
      where: { apiKey },
    });

    if (!website || website.status !== 'active') {
      return res.status(403).json({ error: 'Invalid or inactive widget.' });
    }

    // Quota check
    const limits = { free: 100, pro: 5000, business: Infinity };
    const limit = limits[website.plan] || 100;
    const now = new Date();
    const resetAt = new Date(website.messageResetAt);

    let currentCount = website.messageCount;
    if (
      now.getMonth() !== resetAt.getMonth() ||
      now.getFullYear() !== resetAt.getFullYear()
    ) {
      await prisma.website.update({
        where: { id: website.id },
        data: { messageCount: 0, messageResetAt: now },
      });
      currentCount = 0;
    }

    if (currentCount >= limit) {
      return res
        .status(429)
        .json({ error: 'Message limit reached. Please upgrade your plan.' });
    }

    const conversation = await prisma.conversation.findFirst({
      where: { id: conversationId, websiteId: website.id },
    });

    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found.' });
    }

    const startTime = Date.now();

    await prisma.message.create({
      data: { conversationId, content: message.trim(), role: 'user' },
    });

    const history = await prisma.message.findMany({
      where: { conversationId },
      orderBy: { timestamp: 'asc' },
      take: 10,
    });

    const knowledgeItems = await prisma.knowledgeBaseItem.findMany({
      where: { websiteId: website.id },
    });

    const aiResponse = await generateResponse(
      knowledgeItems,
      history.map((m) => ({ role: m.role, content: m.content })),
      message,
      website.name
    );

    const responseTimeMs = Date.now() - startTime;

    await prisma.message.create({
      data: { conversationId, content: aiResponse, role: 'assistant', responseTimeMs },
    });

    await prisma.website.update({
      where: { id: website.id },
      data: { messageCount: { increment: 1 } },
    });

    updateAnalytics(website.id, responseTimeMs).catch((err) =>
      logger.error('Analytics update failed', { error: err.message })
    );

    res.json({ response: aiResponse, conversationId });
  } catch (error) {
    logger.error('Widget chat error', { error: error.message });
    res.status(500).json({ error: 'Failed to process message.' });
  }
});

/**
 * POST /api/widget/rate
 */
router.post('/rate', async (req, res) => {
  try {
    const { conversationId, rating, apiKey } = req.body;

    if (!conversationId || rating === undefined || !apiKey) {
      return res
        .status(400)
        .json({ error: 'conversationId, rating, and apiKey are required.' });
    }

    if (typeof conversationId !== 'string' || conversationId.length > 100) {
      return res.status(400).json({ error: 'Invalid conversationId.' });
    }

    if (typeof apiKey !== 'string' || apiKey.length < 10 || apiKey.length > 200) {
      return res.status(400).json({ error: 'Invalid apiKey format.' });
    }

    const ratingNum = parseInt(rating);
    if (isNaN(ratingNum) || ratingNum < 1 || ratingNum > 5) {
      return res.status(400).json({ error: 'Rating must be between 1 and 5.' });
    }

    const website = await prisma.website.findUnique({ where: { apiKey } });
    if (!website) {
      return res.status(403).json({ error: 'Invalid API key.' });
    }

    await prisma.conversation.update({
      where: { id: conversationId },
      data: { rating: ratingNum },
    });

    const ratedConversations = await prisma.conversation.findMany({
      where: { websiteId: website.id, rating: { not: null } },
      select: { rating: true },
    });

    if (ratedConversations.length > 0) {
      const avgRating =
        ratedConversations.reduce((sum, c) => sum + c.rating, 0) /
        ratedConversations.length;
      await prisma.analytics.upsert({
        where: { websiteId: website.id },
        update: { satisfactionRate: avgRating },
        create: { websiteId: website.id, satisfactionRate: avgRating },
      });
    }

    res.json({ success: true });
  } catch (error) {
    logger.error('Rating error', { error: error.message });
    res.status(500).json({ error: 'Failed to save rating.' });
  }
});

async function updateAnalytics(websiteId, responseTimeMs) {
  const analytics = await prisma.analytics.findUnique({ where: { websiteId } });
  if (!analytics) {
    await prisma.analytics.create({
      data: { websiteId, totalMessages: 1, avgResponseTime: responseTimeMs },
    });
    return;
  }

  const totalMessages = analytics.totalMessages + 1;
  const avgResponseTime =
    analytics.avgResponseTime +
    (responseTimeMs - analytics.avgResponseTime) / totalMessages;

  await prisma.analytics.update({
    where: { websiteId },
    data: { totalMessages, avgResponseTime },
  });
}

module.exports = router;

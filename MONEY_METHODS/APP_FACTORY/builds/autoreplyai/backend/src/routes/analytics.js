const express = require('express');
const { PrismaClient } = require('@prisma/client');
const { authenticateApiKey } = require('../middleware/auth');
const logger = require('../lib/logger');

const router = express.Router();
const prisma = new PrismaClient();

router.use(authenticateApiKey);

/**
 * GET /api/analytics/overview
 */
router.get('/overview', async (req, res) => {
  try {
    const websiteId = req.website.id;

    const analytics = await prisma.analytics.findUnique({ where: { websiteId } });

    const totalConversations = await prisma.conversation.count({ where: { websiteId } });
    const totalMessages = await prisma.message.count({
      where: { conversation: { websiteId } },
    });

    const todayStart = new Date();
    todayStart.setHours(0, 0, 0, 0);
    const messagesToday = await prisma.message.count({
      where: {
        conversation: { websiteId },
        timestamp: { gte: todayStart },
      },
    });

    const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
    const activeConversations = await prisma.conversation.count({
      where: { websiteId, updatedAt: { gte: oneDayAgo } },
    });

    res.json({
      totalConversations,
      totalMessages,
      messagesToday,
      activeConversations,
      avgResponseTime: analytics?.avgResponseTime || 0,
      satisfactionRate: analytics?.satisfactionRate || 0,
      plan: req.website.plan,
      messageCount: req.website.messageCount,
      messageLimits: { free: 100, pro: 5000, business: -1 },
    });
  } catch (error) {
    logger.error('Analytics overview error', { error: error.message });
    res.status(500).json({ error: 'Failed to fetch analytics.' });
  }
});

/**
 * GET /api/analytics/messages-per-day
 */
router.get('/messages-per-day', async (req, res) => {
  try {
    const days = Math.min(parseInt(req.query.days) || 30, 90);
    const websiteId = req.website.id;
    const since = new Date(Date.now() - days * 24 * 60 * 60 * 1000);

    const messages = await prisma.message.findMany({
      where: {
        conversation: { websiteId },
        timestamp: { gte: since },
      },
      select: { timestamp: true },
      orderBy: { timestamp: 'asc' },
    });

    const byDay = {};
    for (let i = 0; i < days; i++) {
      const d = new Date(Date.now() - (days - 1 - i) * 24 * 60 * 60 * 1000);
      const key = d.toISOString().split('T')[0];
      byDay[key] = 0;
    }

    messages.forEach((m) => {
      const key = m.timestamp.toISOString().split('T')[0];
      if (byDay[key] !== undefined) byDay[key]++;
    });

    res.json({
      data: Object.entries(byDay).map(([date, count]) => ({ date, count })),
    });
  } catch (error) {
    logger.error('Messages per day error', { error: error.message });
    res.status(500).json({ error: 'Failed to fetch message stats.' });
  }
});

/**
 * GET /api/analytics/conversations
 */
router.get('/conversations', async (req, res) => {
  try {
    const { search, page = 1, limit = 20 } = req.query;

    if (search && (typeof search !== 'string' || search.length > 200)) {
      return res.status(400).json({ error: 'Search query must be under 200 characters.' });
    }

    const parsedPage = Math.max(1, parseInt(page) || 1);
    const parsedLimit = Math.min(Math.max(1, parseInt(limit) || 20), 100);
    const skip = (parsedPage - 1) * parsedLimit;
    const take = parsedLimit;
    const websiteId = req.website.id;

    const where = { websiteId };

    const [conversations, total] = await Promise.all([
      prisma.conversation.findMany({
        where,
        include: {
          messages: {
            orderBy: { timestamp: 'asc' },
            take: 50,
          },
        },
        orderBy: { updatedAt: 'desc' },
        skip,
        take,
      }),
      prisma.conversation.count({ where }),
    ]);

    let filtered = conversations;
    if (search && typeof search === 'string') {
      const searchLower = search.toLowerCase();
      filtered = conversations.filter((c) =>
        c.messages.some((m) => m.content.toLowerCase().includes(searchLower))
      );
    }

    res.json({
      conversations: filtered.map((c) => ({
        id: c.id,
        status: c.status,
        rating: c.rating,
        messageCount: c.messages.length,
        lastMessage: c.messages[c.messages.length - 1]?.content || '',
        createdAt: c.createdAt,
        updatedAt: c.updatedAt,
        messages: c.messages,
      })),
      total,
      page: parsedPage,
      totalPages: Math.ceil(total / take),
    });
  } catch (error) {
    logger.error('Conversations list error', { error: error.message });
    res.status(500).json({ error: 'Failed to fetch conversations.' });
  }
});

/**
 * GET /api/analytics/conversations/:id
 */
router.get('/conversations/:id', async (req, res) => {
  try {
    if (!req.params.id || typeof req.params.id !== 'string' || req.params.id.length > 100) {
      return res.status(400).json({ error: 'Invalid conversation ID.' });
    }

    const conversation = await prisma.conversation.findFirst({
      where: { id: req.params.id, websiteId: req.website.id },
      include: {
        messages: { orderBy: { timestamp: 'asc' } },
      },
    });

    if (!conversation) {
      return res.status(404).json({ error: 'Conversation not found.' });
    }

    res.json(conversation);
  } catch (error) {
    logger.error('Get conversation error', { error: error.message });
    res.status(500).json({ error: 'Failed to fetch conversation.' });
  }
});

module.exports = router;

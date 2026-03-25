const express = require('express');
const { PrismaClient } = require('@prisma/client');
const { authenticateApiKey } = require('../middleware/auth');
const logger = require('../lib/logger');

const router = express.Router();
const prisma = new PrismaClient();

router.use(authenticateApiKey);

/**
 * GET /api/knowledge
 */
router.get('/', async (req, res) => {
  try {
    const items = await prisma.knowledgeBaseItem.findMany({
      where: { websiteId: req.website.id },
      orderBy: { updatedAt: 'desc' },
    });

    res.json({ items, total: items.length });
  } catch (error) {
    logger.error('List knowledge error', { error: error.message });
    res.status(500).json({ error: 'Failed to list knowledge base items.' });
  }
});

/**
 * POST /api/knowledge
 */
router.post('/', async (req, res) => {
  try {
    const { title, content, type } = req.body;

    if (!title || !content) {
      return res.status(400).json({ error: 'title and content are required.' });
    }

    if (typeof title !== 'string' || title.length > 500) {
      return res.status(400).json({ error: 'Title must be under 500 characters.' });
    }

    if (typeof content !== 'string' || content.length > 10000) {
      return res.status(400).json({ error: 'Content must be under 10,000 characters.' });
    }

    const validTypes = ['faq', 'page', 'custom'];
    const itemType = validTypes.includes(type) ? type : 'faq';

    const item = await prisma.knowledgeBaseItem.create({
      data: {
        title: title.trim(),
        content: content.trim(),
        type: itemType,
        websiteId: req.website.id,
      },
    });

    res.status(201).json(item);
  } catch (error) {
    logger.error('Create knowledge error', { error: error.message });
    res.status(500).json({ error: 'Failed to create knowledge base item.' });
  }
});

/**
 * POST /api/knowledge/bulk
 */
router.post('/bulk', async (req, res) => {
  try {
    const { items } = req.body;

    if (!Array.isArray(items) || items.length === 0) {
      return res.status(400).json({ error: 'items array is required.' });
    }

    if (items.length > 100) {
      return res.status(400).json({ error: 'Max 100 items per bulk import.' });
    }

    // Validate each item
    for (const item of items) {
      if (!item.title || !item.content) {
        return res.status(400).json({ error: 'Each item must have a title and content.' });
      }
    }

    const created = await prisma.knowledgeBaseItem.createMany({
      data: items.map((item) => ({
        title: String(item.title).trim().slice(0, 500),
        content: String(item.content).trim().slice(0, 10000),
        type: ['faq', 'page', 'custom'].includes(item.type) ? item.type : 'faq',
        websiteId: req.website.id,
      })),
    });

    logger.info('Bulk knowledge import', {
      websiteId: req.website.id,
      count: created.count,
    });

    res.status(201).json({ created: created.count });
  } catch (error) {
    logger.error('Bulk create error', { error: error.message });
    res.status(500).json({ error: 'Failed to bulk create items.' });
  }
});

/**
 * GET /api/knowledge/:id
 */
router.get('/:id', async (req, res) => {
  try {
    if (!req.params.id || typeof req.params.id !== 'string' || req.params.id.length > 100) {
      return res.status(400).json({ error: 'Invalid item ID.' });
    }

    const item = await prisma.knowledgeBaseItem.findFirst({
      where: { id: req.params.id, websiteId: req.website.id },
    });

    if (!item) {
      return res.status(404).json({ error: 'Item not found.' });
    }

    res.json(item);
  } catch (error) {
    logger.error('Get knowledge error', { error: error.message });
    res.status(500).json({ error: 'Failed to get item.' });
  }
});

/**
 * PUT /api/knowledge/:id
 */
router.put('/:id', async (req, res) => {
  try {
    if (!req.params.id || typeof req.params.id !== 'string' || req.params.id.length > 100) {
      return res.status(400).json({ error: 'Invalid item ID.' });
    }

    const { title, content, type } = req.body;

    const existing = await prisma.knowledgeBaseItem.findFirst({
      where: { id: req.params.id, websiteId: req.website.id },
    });

    if (!existing) {
      return res.status(404).json({ error: 'Item not found.' });
    }

    const updated = await prisma.knowledgeBaseItem.update({
      where: { id: req.params.id },
      data: {
        ...(title && { title: String(title).trim().slice(0, 500) }),
        ...(content && { content: String(content).trim().slice(0, 10000) }),
        ...(type && ['faq', 'page', 'custom'].includes(type) && { type }),
      },
    });

    res.json(updated);
  } catch (error) {
    logger.error('Update knowledge error', { error: error.message });
    res.status(500).json({ error: 'Failed to update item.' });
  }
});

/**
 * DELETE /api/knowledge/:id
 */
router.delete('/:id', async (req, res) => {
  try {
    if (!req.params.id || typeof req.params.id !== 'string' || req.params.id.length > 100) {
      return res.status(400).json({ error: 'Invalid item ID.' });
    }

    const existing = await prisma.knowledgeBaseItem.findFirst({
      where: { id: req.params.id, websiteId: req.website.id },
    });

    if (!existing) {
      return res.status(404).json({ error: 'Item not found.' });
    }

    await prisma.knowledgeBaseItem.delete({
      where: { id: req.params.id },
    });

    res.json({ success: true });
  } catch (error) {
    logger.error('Delete knowledge error', { error: error.message });
    res.status(500).json({ error: 'Failed to delete item.' });
  }
});

module.exports = router;

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const path = require('path');
const { PrismaClient } = require('@prisma/client');
const logger = require('./lib/logger');

const authRoutes = require('./routes/auth');
const widgetRoutes = require('./routes/widget');
const knowledgeRoutes = require('./routes/knowledge');
const analyticsRoutes = require('./routes/analytics');
const billingRoutes = require('./routes/billing');

const app = express();
const prisma = new PrismaClient();

// Trust proxy for rate limiting behind reverse proxy
app.set('trust proxy', 1);

// Global rate limiter
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 500,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later.' },
});

// Stricter rate limiter for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 30,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many authentication attempts. Please try again later.' },
});

// Stripe webhook needs raw body - must come before express.json()
app.use('/api/billing/webhook', express.raw({ type: 'application/json' }));

// Middleware
app.use(
  helmet({
    crossOriginResourcePolicy: { policy: 'cross-origin' },
    contentSecurityPolicy: false,
  })
);

const allowedOrigins = process.env.NODE_ENV === 'production'
  ? [process.env.CORS_ORIGIN].filter(Boolean)
  : ['http://localhost:3000', 'http://localhost:3001'];

app.use(
  cors({
    origin: process.env.NODE_ENV === 'production'
      ? (origin, callback) => {
          if (!origin || allowedOrigins.includes(origin) || /\.autoreplyai\.com$/.test(origin || '')) {
            callback(null, true);
          } else {
            callback(null, false);
          }
        }
      : '*',
    credentials: true,
  })
);

app.use(express.json({ limit: '10mb' }));

// Morgan logging stream through winston
const morganStream = {
  write: (message) => logger.info(message.trim()),
};
app.use(
  morgan(process.env.NODE_ENV === 'production' ? 'combined' : 'dev', {
    stream: morganStream,
    skip: (req) => req.path === '/health',
  })
);

app.use(globalLimiter);

// Make prisma available to routes
app.locals.prisma = prisma;

// Serve widget static files
app.use('/widget', express.static(path.join(__dirname, '..', 'widget')));

// Health check
app.get('/health', async (req, res) => {
  try {
    await prisma.$queryRaw`SELECT 1`;
    res.json({
      status: 'ok',
      database: 'connected',
      timestamp: new Date().toISOString(),
    });
  } catch {
    res.status(500).json({ status: 'error', database: 'disconnected' });
  }
});

// API Routes
app.use('/api/auth', authLimiter, authRoutes);
app.use('/api/widget', widgetRoutes);
app.use('/api/knowledge', knowledgeRoutes);
app.use('/api/analytics', analyticsRoutes);
app.use('/api/billing', billingRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// Global error handling middleware
app.use((err, req, res, _next) => {
  const status = err.status || err.statusCode || 500;
  const message =
    process.env.NODE_ENV === 'production' && status === 500
      ? 'Internal server error'
      : err.message || 'Something went wrong';

  if (status >= 500) {
    logger.error('Unhandled error', {
      message: err.message,
      stack: err.stack,
      path: req.path,
      method: req.method,
    });
  }

  res.status(status).json({ error: message });
});

// Graceful shutdown
const shutdown = async (signal) => {
  logger.info(`${signal} received, shutting down gracefully...`);
  await prisma.$disconnect();
  process.exit(0);
};

process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));

process.on('unhandledRejection', (reason) => {
  logger.error('Unhandled promise rejection', { reason: String(reason) });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  logger.info(`AutoReplyAI backend running on port ${PORT}`);
  logger.info(`Environment: ${process.env.NODE_ENV || 'development'}`);
});

module.exports = app;

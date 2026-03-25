const express = require('express');
const { PrismaClient } = require('@prisma/client');
const { authenticateApiKey } = require('../middleware/auth');
const logger = require('../lib/logger');

const router = express.Router();
const prisma = new PrismaClient();

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

const PLANS = {
  free: {
    name: 'Free',
    price: 0,
    messages: 100,
    stripePriceId: null,
  },
  pro: {
    name: 'Pro',
    price: 1900,
    messages: 5000,
    stripePriceId: process.env.STRIPE_PRO_PRICE_ID || null,
  },
  business: {
    name: 'Business',
    price: 4900,
    messages: -1,
    stripePriceId: process.env.STRIPE_BUSINESS_PRICE_ID || null,
  },
};

/**
 * GET /api/billing/plans
 */
router.get('/plans', (req, res) => {
  res.json({
    plans: Object.entries(PLANS).map(([key, plan]) => ({
      id: key,
      name: plan.name,
      price: plan.price / 100,
      messagesPerMonth: plan.messages === -1 ? 'Unlimited' : plan.messages,
      features: getPlanFeatures(key),
    })),
  });
});

/**
 * POST /api/billing/checkout
 */
router.post('/checkout', authenticateApiKey, async (req, res) => {
  try {
    const { plan } = req.body;

    if (!plan || typeof plan !== 'string' || !PLANS[plan] || plan === 'free') {
      return res.status(400).json({ error: 'Invalid plan. Choose pro or business.' });
    }

    const website = req.website;

    let customerId = website.stripeCustomerId;
    if (!customerId) {
      const customer = await stripe.customers.create({
        email: website.email,
        metadata: { websiteId: website.id, websiteName: website.name },
      });
      customerId = customer.id;
      await prisma.website.update({
        where: { id: website.id },
        data: { stripeCustomerId: customerId },
      });
    }

    // Use pre-configured Stripe Price ID if available, otherwise create dynamically
    let priceId = PLANS[plan].stripePriceId;
    if (!priceId) {
      const price = await stripe.prices.create({
        unit_amount: PLANS[plan].price,
        currency: 'usd',
        recurring: { interval: 'month' },
        product_data: {
          name: `AutoReplyAI ${PLANS[plan].name} Plan`,
        },
      });
      priceId = price.id;
    }

    const session = await stripe.checkout.sessions.create({
      customer: customerId,
      payment_method_types: ['card'],
      line_items: [{ price: priceId, quantity: 1 }],
      mode: 'subscription',
      success_url: `${process.env.CORS_ORIGIN || 'http://localhost:3000'}/dashboard/billing?success=true`,
      cancel_url: `${process.env.CORS_ORIGIN || 'http://localhost:3000'}/dashboard/billing?canceled=true`,
      metadata: { websiteId: website.id, plan },
    });

    logger.info('Checkout session created', {
      websiteId: website.id,
      plan,
      sessionId: session.id,
    });

    res.json({ url: session.url, sessionId: session.id });
  } catch (error) {
    logger.error('Checkout error', { error: error.message });
    res.status(500).json({ error: 'Failed to create checkout session.' });
  }
});

/**
 * POST /api/billing/portal
 */
router.post('/portal', authenticateApiKey, async (req, res) => {
  try {
    if (!req.website.stripeCustomerId) {
      return res
        .status(400)
        .json({ error: 'No billing account found. Subscribe to a plan first.' });
    }

    const session = await stripe.billingPortal.sessions.create({
      customer: req.website.stripeCustomerId,
      return_url: `${process.env.CORS_ORIGIN || 'http://localhost:3000'}/dashboard/billing`,
    });

    res.json({ url: session.url });
  } catch (error) {
    logger.error('Portal error', { error: error.message });
    res.status(500).json({ error: 'Failed to create portal session.' });
  }
});

/**
 * GET /api/billing/status
 */
router.get('/status', authenticateApiKey, async (req, res) => {
  try {
    const website = req.website;
    const result = {
      plan: website.plan,
      messageCount: website.messageCount,
      messageLimit: PLANS[website.plan]?.messages || 100,
      stripeCustomerId: website.stripeCustomerId || null,
      subscription: null,
    };

    if (website.stripeSubId) {
      try {
        const sub = await stripe.subscriptions.retrieve(website.stripeSubId);
        result.subscription = {
          status: sub.status,
          currentPeriodEnd: new Date(sub.current_period_end * 1000),
          cancelAtPeriodEnd: sub.cancel_at_period_end,
        };
      } catch {
        result.subscription = null;
      }
    }

    res.json(result);
  } catch (error) {
    logger.error('Billing status error', { error: error.message });
    res.status(500).json({ error: 'Failed to fetch billing status.' });
  }
});

/**
 * POST /api/billing/webhook
 * Stripe webhook with signature validation.
 */
router.post('/webhook', async (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;

  try {
    if (process.env.STRIPE_WEBHOOK_SECRET) {
      event = stripe.webhooks.constructEvent(
        req.body,
        sig,
        process.env.STRIPE_WEBHOOK_SECRET
      );
    } else {
      // Dev mode without webhook secret
      event = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
      logger.warn('Stripe webhook processed without signature verification (dev mode)');
    }
  } catch (err) {
    logger.error('Webhook signature verification failed', { error: err.message });
    return res.status(400).json({ error: 'Webhook signature verification failed.' });
  }

  try {
    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object;
        const { websiteId, plan } = session.metadata || {};
        if (websiteId && plan) {
          await prisma.website.update({
            where: { id: websiteId },
            data: {
              plan,
              stripeSubId: session.subscription,
              stripeCustomerId: session.customer,
            },
          });
          logger.info('Plan upgraded', { websiteId, plan });
        }
        break;
      }

      case 'customer.subscription.updated': {
        const sub = event.data.object;
        const website = await prisma.website.findFirst({
          where: { stripeSubId: sub.id },
        });
        if (website && sub.status === 'active') {
          logger.info('Subscription updated', { websiteId: website.id });
        }
        break;
      }

      case 'customer.subscription.deleted': {
        const sub = event.data.object;
        const website = await prisma.website.findFirst({
          where: { stripeSubId: sub.id },
        });
        if (website) {
          await prisma.website.update({
            where: { id: website.id },
            data: { plan: 'free', stripeSubId: null },
          });
          logger.info('Subscription canceled, downgraded to free', {
            websiteId: website.id,
          });
        }
        break;
      }

      case 'invoice.payment_failed': {
        const invoice = event.data.object;
        logger.warn('Payment failed', { customerId: invoice.customer });
        break;
      }

      default:
        logger.debug('Unhandled webhook event', { type: event.type });
    }

    res.json({ received: true });
  } catch (error) {
    logger.error('Webhook processing error', { error: error.message });
    res.status(500).json({ error: 'Webhook processing failed.' });
  }
});

function getPlanFeatures(plan) {
  const features = {
    free: [
      '100 messages/month',
      'Basic AI responses',
      'Single widget',
      'Community support',
    ],
    pro: [
      '5,000 messages/month',
      'Advanced AI with knowledge base',
      'Analytics dashboard',
      'Widget customization',
      'Email support',
    ],
    business: [
      'Unlimited messages',
      'Priority AI processing',
      'Full analytics suite',
      'Custom branding',
      'Priority support',
      'API access',
    ],
  };
  return features[plan] || features.free;
}

module.exports = router;

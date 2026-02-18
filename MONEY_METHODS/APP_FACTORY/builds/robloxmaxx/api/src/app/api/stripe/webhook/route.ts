import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { getDb } from '@/services/db';

function getStripe() {
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) throw new Error('STRIPE_SECRET_KEY not set');
  return new Stripe(key);
}

// BYOK model: plans control platform ACCESS, not API credits.
// Free: plugin + basic code gen (BYOK)
// Pro ($9.99/mo): meta advisor, revenue estimator, game scanner, premium templates
// Users always bring their own API key. Zero API cost to us.

export async function POST(request: NextRequest) {
  const body = await request.text();
  const sig = request.headers.get('stripe-signature');

  if (!sig) {
    return NextResponse.json({ error: 'No signature' }, { status: 400 });
  }

  let event: Stripe.Event;
  const stripe = getStripe();

  try {
    event = stripe.webhooks.constructEvent(
      body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET || ''
    );
  } catch (err) {
    console.error('[Stripe] Webhook signature verification failed');
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }

  const db = getDb();

  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.Checkout.Session;
      const customerId = session.customer as string;
      const plan = (session.metadata?.plan as string) || 'pro';

      db.prepare(
        `UPDATE users SET plan = ?, stripe_customer_id = ?, updated_at = datetime('now')
         WHERE stripe_customer_id = ? OR email = ?`
      ).run(
        plan,
        customerId,
        customerId,
        session.customer_email || ''
      );
      break;
    }

    case 'customer.subscription.deleted': {
      const subscription = event.data.object as Stripe.Subscription;
      const customerId = subscription.customer as string;

      db.prepare(
        `UPDATE users SET plan = 'free', updated_at = datetime('now')
         WHERE stripe_customer_id = ?`
      ).run(customerId);
      break;
    }
  }

  return NextResponse.json({ received: true });
}

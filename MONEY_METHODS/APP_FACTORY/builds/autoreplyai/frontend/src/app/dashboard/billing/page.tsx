'use client';

import { Suspense, useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import api from '@/lib/api';
import { useToast } from '@/components/Toast';
import { Skeleton } from '@/components/Skeleton';

interface Plan {
  id: string;
  name: string;
  price: number;
  messagesPerMonth: number | string;
  features: string[];
}

interface BillingStatus {
  plan: string;
  messageCount: number;
  messageLimit: number;
  subscription: {
    status: string;
    currentPeriodEnd: string;
    cancelAtPeriodEnd: boolean;
  } | null;
}

function BillingLoadingSkeleton() {
  return (
    <div className="space-y-6 max-w-4xl">
      <div className="card p-6 space-y-4">
        <Skeleton className="h-5 w-32" />
        <Skeleton className="h-8 w-24" />
        <Skeleton className="h-3 w-48" />
      </div>
      <div className="grid md:grid-cols-3 gap-4">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="card p-6 space-y-4">
            <Skeleton className="h-5 w-24" />
            <Skeleton className="h-8 w-16" />
            <div className="space-y-2">
              {Array.from({ length: 4 }).map((_, j) => (
                <Skeleton key={j} className="h-3 w-full" />
              ))}
            </div>
            <Skeleton className="h-10 w-full rounded-lg" />
          </div>
        ))}
      </div>
    </div>
  );
}

export default function BillingPageWrapper() {
  return (
    <Suspense fallback={<BillingLoadingSkeleton />}>
      <BillingPage />
    </Suspense>
  );
}

function BillingPage() {
  const searchParams = useSearchParams();
  const toast = useToast();
  const [plans, setPlans] = useState<Plan[]>([]);
  const [billing, setBilling] = useState<BillingStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [upgrading, setUpgrading] = useState<string | null>(null);

  const success = searchParams.get('success') === 'true';
  const canceled = searchParams.get('canceled') === 'true';

  useEffect(() => {
    if (success) toast.success('Subscription Active', 'Your plan has been upgraded.');
    if (canceled) toast.warning('Checkout Canceled', 'No charges were made.');
  }, [success, canceled, toast]);

  useEffect(() => {
    Promise.all([api.getPlans(), api.getBillingStatus()])
      .then(([plansData, billingData]) => {
        setPlans(plansData.plans || []);
        setBilling(billingData);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleUpgrade = async (planId: string) => {
    setUpgrading(planId);
    try {
      const data = await api.createCheckout(planId);
      if (data.url) {
        window.location.href = data.url;
      }
    } catch {
      // Toast handled by API client
      setUpgrading(null);
    }
  };

  const handleManage = async () => {
    try {
      const data = await api.getBillingPortal();
      if (data.url) {
        window.location.href = data.url;
      }
    } catch {
      // Toast handled by API client
    }
  };

  if (loading) return <BillingLoadingSkeleton />;

  const usagePct = billing
    ? billing.messageLimit > 0
      ? Math.min((billing.messageCount / billing.messageLimit) * 100, 100)
      : 0
    : 0;

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Current Plan */}
      {billing && (
        <div className="card p-6 animate-fade-in">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <h2 className="section-heading text-sm">Current Plan</h2>
                <span className={`badge text-[10px] uppercase ${
                  billing.plan === 'business' ? 'badge-yellow' :
                  billing.plan === 'pro' ? 'badge-blue' : 'badge-gray'
                }`}>
                  {billing.plan}
                </span>
              </div>

              {/* Usage bar */}
              <div className="flex items-center gap-3 mb-2">
                <div className="w-48 bg-surface-300 rounded-full h-1.5">
                  <div
                    className={`h-1.5 rounded-full transition-all duration-500 ${
                      usagePct > 90 ? 'bg-danger-500' : usagePct > 70 ? 'bg-warning-500' : 'bg-brand-500'
                    }`}
                    style={{ width: `${usagePct}%` }}
                  />
                </div>
                <span className="text-xs text-gray-500 font-mono whitespace-nowrap">
                  {billing.messageCount.toLocaleString()} /{' '}
                  {billing.messageLimit === -1 ? 'Unlimited' : billing.messageLimit.toLocaleString()}
                </span>
              </div>

              {billing.subscription && (
                <p className="text-xs text-gray-600">
                  {billing.subscription.cancelAtPeriodEnd ? 'Cancels' : 'Renews'} on{' '}
                  {new Date(billing.subscription.currentPeriodEnd).toLocaleDateString(undefined, {
                    month: 'long',
                    day: 'numeric',
                    year: 'numeric',
                  })}
                </p>
              )}
            </div>

            {billing.subscription && (
              <button onClick={handleManage} className="btn-secondary text-xs py-2">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 011.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 01-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.397.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 01-.12-1.45l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.506-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.107-1.204l-.527-.738a1.125 1.125 0 01.12-1.45l.773-.773a1.125 1.125 0 011.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894z" />
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Manage Subscription
              </button>
            )}
          </div>
        </div>
      )}

      {/* Plans */}
      <div>
        <h2 className="section-heading text-sm mb-4">Available Plans</h2>
        <div className="grid md:grid-cols-3 gap-4">
          {plans.map((plan) => {
            const isCurrent = billing?.plan === plan.id;
            const isUpgrade = plan.price > 0 && !isCurrent;
            const isFeatured = plan.id === 'pro';

            return (
              <div
                key={plan.id}
                className={`relative rounded-xl p-6 transition-all duration-200 animate-fade-in ${
                  isCurrent
                    ? 'bg-brand-500/10 border-2 border-brand-500/30'
                    : isFeatured
                    ? 'card border-brand-500/20 shadow-lg shadow-brand-500/5'
                    : 'card'
                }`}
              >
                {isFeatured && !isCurrent && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <span className="bg-brand-500 text-white text-[10px] font-semibold px-3 py-1 rounded-full shadow-lg shadow-brand-500/30">
                      Recommended
                    </span>
                  </div>
                )}

                <div className="mb-5">
                  <h3 className="text-base font-semibold text-white">{plan.name}</h3>
                  <div className="mt-2">
                    <span className="text-3xl font-bold text-white">
                      {plan.price === 0 ? 'Free' : `$${plan.price}`}
                    </span>
                    {plan.price > 0 && (
                      <span className="text-sm text-gray-500 ml-1">/mo</span>
                    )}
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    {typeof plan.messagesPerMonth === 'number'
                      ? `${plan.messagesPerMonth.toLocaleString()} messages/month`
                      : plan.messagesPerMonth}
                  </p>
                </div>

                <ul className="space-y-2.5 mb-6">
                  {plan.features.map((f, i) => (
                    <li key={i} className="flex items-start gap-2 text-xs text-gray-300">
                      <svg
                        className="w-3.5 h-3.5 text-success-400 mt-0.5 flex-shrink-0"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth={2.5}
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                      {f}
                    </li>
                  ))}
                </ul>

                {isCurrent ? (
                  <div className="text-center py-2.5 text-xs text-brand-400 font-medium border border-brand-500/20 rounded-lg bg-brand-500/5">
                    Current Plan
                  </div>
                ) : isUpgrade ? (
                  <button
                    onClick={() => handleUpgrade(plan.id)}
                    disabled={upgrading === plan.id}
                    className={`w-full py-2.5 text-xs font-semibold rounded-lg transition-all ${
                      isFeatured
                        ? 'btn-primary'
                        : 'btn-secondary'
                    }`}
                  >
                    {upgrading === plan.id ? (
                      <div className="flex items-center justify-center gap-2">
                        <svg className="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                        </svg>
                        Redirecting...
                      </div>
                    ) : (
                      `Upgrade to ${plan.name}`
                    )}
                  </button>
                ) : (
                  <div className="text-center py-2.5 text-xs text-gray-600">
                    Free Forever
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* FAQ */}
      <div className="card p-6">
        <h3 className="section-heading text-sm mb-3">Billing FAQ</h3>
        <div className="space-y-3 text-xs">
          <div>
            <p className="text-gray-300 font-medium">How does billing work?</p>
            <p className="text-gray-500 mt-0.5">Plans are billed monthly via Stripe. You can upgrade, downgrade, or cancel at any time.</p>
          </div>
          <div>
            <p className="text-gray-300 font-medium">What happens when I hit my message limit?</p>
            <p className="text-gray-500 mt-0.5">Your widget will gracefully inform visitors to try again later. No extra charges are incurred.</p>
          </div>
          <div>
            <p className="text-gray-300 font-medium">Can I get a refund?</p>
            <p className="text-gray-500 mt-0.5">We offer a 14-day money-back guarantee on all paid plans. Contact support for assistance.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

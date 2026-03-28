import type { ViewName } from '../types';

interface PaywallProps {
  navigate: (view: ViewName) => void;
  onActivate: () => void;
}

const ANNUAL_LINK = 'https://buy.stripe.com/5kQcN60nm8RLblL05h3F60D';
const MONTHLY_LINK = 'https://buy.stripe.com/5kQ14o6LK04f4bneWa3F60E';

export default function Paywall({ navigate, onActivate }: PaywallProps) {
  const handlePurchase = (url: string) => {
    window.open(url, '_blank');
  };

  return (
    <div className="min-h-screen bg-navy flex flex-col">
      {/* Close */}
      <div className="p-4">
        <button
          onClick={() => navigate('dashboard')}
          className="text-gray-400 flex items-center gap-1"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
          Close
        </button>
      </div>

      <div className="flex-1 flex flex-col items-center justify-center px-4 pb-8 max-w-lg mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 rounded-2xl bg-coral/20 flex items-center justify-center mx-auto mb-4">
            <svg viewBox="0 0 40 40" className="w-10 h-10" fill="none">
              <path d="M20 4L8 10v10c0 8.4 5.12 16.24 12 18 6.88-1.76 12-9.6 12-18V10L20 4z" stroke="#e94560" strokeWidth="2.5" fill="none" />
              <path d="M14 20l4 4 8-8" stroke="#e94560" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">Upgrade to Pro</h1>
          <p className="text-gray-400">Unlock the full power of cnsnt</p>
        </div>

        {/* Features */}
        <div className="w-full space-y-3 mb-8">
          {[
            'Unlimited consent records',
            'All 11 premium templates',
            'PDF export with signatures',
            'Priority support',
            'Encrypted cloud backup',
          ].map((feature) => (
            <div key={feature} className="flex items-center gap-3">
              <svg className="w-5 h-5 text-coral flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
              </svg>
              <span className="text-white">{feature}</span>
            </div>
          ))}
        </div>

        {/* Trial timeline */}
        <div className="w-full bg-navy-light border border-gray-700 rounded-xl p-4 mb-6">
          <div className="flex items-center justify-between mb-3">
            <span className="text-gray-400 text-sm">Today</span>
            <span className="text-gray-400 text-sm">Day 7</span>
          </div>
          <div className="h-2 bg-gray-700 rounded-full overflow-hidden mb-3">
            <div className="h-full bg-gradient-to-r from-green-400 to-coral rounded-full" style={{ width: '15%' }} />
          </div>
          <div className="flex items-center justify-between text-xs">
            <span className="text-green-400 font-medium">Full access starts</span>
            <span className="text-gray-500">First payment</span>
          </div>
          <p className="text-center text-gray-500 text-xs mt-3">No payment due now</p>
        </div>

        {/* Pricing cards */}
        <div className="w-full space-y-3 mb-6">
          {/* Annual - highlighted */}
          <button
            onClick={() => handlePurchase(ANNUAL_LINK)}
            className="w-full bg-coral/10 border-2 border-coral rounded-xl p-4 text-left relative"
          >
            <span className="absolute -top-3 right-4 px-3 py-0.5 bg-coral text-white text-xs font-bold rounded-full">
              BEST VALUE
            </span>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white font-semibold text-lg">Annual</p>
                <p className="text-gray-400 text-sm">$29.99/year</p>
              </div>
              <div className="text-right">
                <p className="text-white font-bold text-2xl">$2.49</p>
                <p className="text-gray-400 text-sm">/month</p>
              </div>
            </div>
            <p className="text-coral text-xs font-medium mt-2">Save 50% vs monthly</p>
          </button>

          {/* Monthly */}
          <button
            onClick={() => handlePurchase(MONTHLY_LINK)}
            className="w-full bg-navy-light border border-gray-700 rounded-xl p-4 text-left"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-white font-semibold text-lg">Monthly</p>
                <p className="text-gray-400 text-sm">Billed monthly</p>
              </div>
              <div className="text-right">
                <p className="text-white font-bold text-2xl">$4.99</p>
                <p className="text-gray-400 text-sm">/month</p>
              </div>
            </div>
          </button>
        </div>

        {/* Activate (honor system) */}
        <button
          onClick={onActivate}
          className="text-gray-500 text-xs underline mb-4"
        >
          Already purchased? Activate Pro
        </button>

        {/* Legal */}
        <div className="text-center space-y-2">
          <p className="text-gray-600 text-xs">
            Payment is processed securely via Stripe. Cancel anytime.
          </p>
          <p className="text-gray-600 text-xs">
            By subscribing, you agree to the{' '}
            <a href="https://printmaxx-tos.surge.sh" target="_blank" rel="noopener noreferrer" className="text-gray-500 underline">
              Terms of Service
            </a>
            {' '}and{' '}
            <a href="https://printmaxx-privacy.surge.sh" target="_blank" rel="noopener noreferrer" className="text-gray-500 underline">
              Privacy Policy
            </a>
          </p>
          <p className="text-gray-600 text-xs">
            Subscriptions auto-renew until cancelled. You can manage your subscription through the Stripe customer portal.
          </p>
        </div>
      </div>
    </div>
  );
}

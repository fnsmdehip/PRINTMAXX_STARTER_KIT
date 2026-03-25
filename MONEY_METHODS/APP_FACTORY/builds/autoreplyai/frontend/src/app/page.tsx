'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import Link from 'next/link';
import Navbar from '@/components/Navbar';

/* ──────────────────────── Animations ──────────────────────── */
const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: (delay: number = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, delay, ease: [0.25, 0.46, 0.45, 0.94] },
  }),
};

const staggerContainer = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12 } },
};

/* ──────────────────────── Section wrapper ──────────────────── */
function Section({
  id,
  children,
  className = '',
  dark = false,
}: {
  id?: string;
  children: React.ReactNode;
  className?: string;
  dark?: boolean;
}) {
  const [ref, inView] = useInView({ triggerOnce: true, threshold: 0.1 });
  return (
    <motion.section
      ref={ref}
      id={id}
      initial="hidden"
      animate={inView ? 'visible' : 'hidden'}
      variants={staggerContainer}
      className={`relative py-24 lg:py-32 ${dark ? 'bg-surface-500/50' : ''} ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">{children}</div>
    </motion.section>
  );
}

/* ──────────────────────── Stat counter ─────────────────────── */
function Stat({ value, label }: { value: string; label: string }) {
  return (
    <motion.div variants={fadeUp} className="text-center">
      <div className="text-4xl lg:text-5xl font-bold text-white mb-2">{value}</div>
      <div className="text-sm text-gray-400 tracking-wide uppercase">{label}</div>
    </motion.div>
  );
}

/* ──────────────────────── Feature card ─────────────────────── */
function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <motion.div
      variants={fadeUp}
      className="group card-hover p-6 lg:p-8"
    >
      <div className="w-12 h-12 rounded-xl bg-brand-500/10 border border-brand-500/20 flex items-center justify-center mb-5 group-hover:bg-brand-500/15 transition-colors">
        {icon}
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
      <p className="text-sm text-gray-400 leading-relaxed">{description}</p>
    </motion.div>
  );
}

/* ──────────────────────── Pricing card ─────────────────────── */
function PricingCard({
  name,
  price,
  period,
  description,
  features,
  cta,
  featured = false,
}: {
  name: string;
  price: string;
  period: string;
  description: string;
  features: string[];
  cta: string;
  featured?: boolean;
}) {
  return (
    <motion.div
      variants={fadeUp}
      className={`relative rounded-2xl p-8 transition-all duration-300 ${
        featured
          ? 'bg-gradient-to-b from-brand-500/20 to-surface-200 border-2 border-brand-500/40 shadow-xl shadow-brand-500/10 scale-[1.02]'
          : 'card-hover'
      }`}
    >
      {featured && (
        <div className="absolute -top-3.5 left-1/2 -translate-x-1/2">
          <span className="bg-brand-500 text-white text-xs font-semibold px-4 py-1.5 rounded-full shadow-lg shadow-brand-500/30">
            Most Popular
          </span>
        </div>
      )}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white mb-1">{name}</h3>
        <p className="text-sm text-gray-500">{description}</p>
      </div>
      <div className="mb-6">
        <span className="text-4xl font-bold text-white">{price}</span>
        <span className="text-gray-500 ml-1">{period}</span>
      </div>
      <ul className="space-y-3 mb-8">
        {features.map((f, i) => (
          <li key={i} className="flex items-start gap-3 text-sm text-gray-300">
            <svg
              className="w-4.5 h-4.5 text-success-400 mt-0.5 flex-shrink-0"
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
      <Link
        href="/signup"
        className={`block text-center w-full py-3 rounded-lg text-sm font-semibold transition-all duration-200 ${
          featured
            ? 'bg-brand-500 text-white hover:bg-brand-600 shadow-lg shadow-brand-500/25'
            : 'bg-white/[0.06] text-gray-300 hover:bg-white/[0.1] hover:text-white border border-white/[0.08]'
        }`}
      >
        {cta}
      </Link>
    </motion.div>
  );
}

/* ──────────────────────── Testimonial card ─────────────────── */
function TestimonialCard({
  quote,
  name,
  role,
  initials,
}: {
  quote: string;
  name: string;
  role: string;
  initials: string;
}) {
  return (
    <motion.div variants={fadeUp} className="card p-6 lg:p-8 flex flex-col">
      <div className="flex gap-1 mb-4">
        {[1, 2, 3, 4, 5].map((s) => (
          <svg key={s} className="w-4 h-4 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        ))}
      </div>
      <p className="text-gray-300 text-sm leading-relaxed flex-1 mb-6">{quote}</p>
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-brand-500/20 border border-brand-500/30 flex items-center justify-center text-sm font-semibold text-brand-400">
          {initials}
        </div>
        <div>
          <div className="text-sm font-medium text-white">{name}</div>
          <div className="text-xs text-gray-500">{role}</div>
        </div>
      </div>
    </motion.div>
  );
}

/* ──────────────────────── FAQ item ─────────────────────────── */
function FAQItem({ question, answer }: { question: string; answer: string }) {
  const [open, setOpen] = useState(false);
  return (
    <motion.div variants={fadeUp} className="border-b border-white/[0.06]">
      <button
        className="flex justify-between items-center w-full text-left py-5 group"
        onClick={() => setOpen(!open)}
        aria-expanded={open}
      >
        <span className="text-[15px] font-medium text-gray-200 group-hover:text-white transition-colors pr-4">
          {question}
        </span>
        <svg
          className={`w-5 h-5 text-gray-500 flex-shrink-0 transition-transform duration-200 ${open ? 'rotate-180' : ''}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      <div
        className={`overflow-hidden transition-all duration-300 ${
          open ? 'max-h-48 pb-5 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <p className="text-sm text-gray-400 leading-relaxed">{answer}</p>
      </div>
    </motion.div>
  );
}

/* ============================== LANDING PAGE ============================== */
export default function Home() {
  return (
    <>
      <Navbar />

      <main className="overflow-hidden">
        {/* ─────── Hero ─────── */}
        <section className="relative min-h-screen flex items-center pt-16">
          {/* Background */}
          <div className="absolute inset-0 bg-grid-pattern bg-grid opacity-40" />
          <div className="absolute inset-0 bg-gradient-to-b from-brand-500/5 via-transparent to-surface" />
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-brand-500/8 rounded-full blur-[120px]" />

          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center py-20">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <span className="inline-flex items-center gap-2 bg-brand-500/10 border border-brand-500/20 rounded-full px-4 py-1.5 text-xs font-medium text-brand-400 mb-8">
                <span className="w-1.5 h-1.5 bg-success-400 rounded-full animate-pulse" />
                Trusted by 2,000+ businesses
              </span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.1 }}
              className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight mb-6"
            >
              <span className="text-white">AI Customer Support</span>
              <br />
              <span className="bg-gradient-to-r from-brand-400 to-blue-300 bg-clip-text text-transparent">
                That Never Sleeps
              </span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.2 }}
              className="text-lg sm:text-xl text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed"
            >
              Deploy an AI agent trained on your knowledge base in under 5 minutes.
              Resolve 90% of support tickets automatically, around the clock.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.35 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
            >
              <Link
                href="/signup"
                className="btn-primary px-8 py-3.5 text-base shadow-lg shadow-brand-500/25 hover:shadow-xl hover:shadow-brand-500/30"
              >
                Start Free Trial
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
              <a
                href="#features"
                className="btn-secondary px-8 py-3.5 text-base"
              >
                See How It Works
              </a>
            </motion.div>

            {/* Hero visual - code snippet */}
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="mt-16 max-w-2xl mx-auto"
            >
              <div className="card overflow-hidden shadow-2xl shadow-black/40">
                <div className="flex items-center gap-2 px-4 py-3 bg-surface-300 border-b border-white/[0.06]">
                  <div className="flex gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-red-500/60" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500/60" />
                    <div className="w-3 h-3 rounded-full bg-green-500/60" />
                  </div>
                  <span className="text-xs text-gray-500 ml-2 font-mono">index.html</span>
                </div>
                <div className="p-5 font-mono text-sm text-left overflow-x-auto">
                  <div className="text-gray-500">&lt;!-- Add to your website --&gt;</div>
                  <div>
                    <span className="text-brand-400">&lt;script</span>{' '}
                    <span className="text-emerald-400">src</span>
                    <span className="text-gray-400">=</span>
                    <span className="text-amber-300">{'"https://cdn.autoreplyai.com/widget.js"'}</span>
                  </div>
                  <div className="pl-4">
                    <span className="text-emerald-400">data-key</span>
                    <span className="text-gray-400">=</span>
                    <span className="text-amber-300">{'"arai_your_key_here"'}</span>
                    <span className="text-brand-400">&gt;&lt;/script&gt;</span>
                  </div>
                  <div className="mt-3 text-gray-500">&lt;!-- That&apos;s it. Seriously. --&gt;</div>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* ─────── Social proof stats ─────── */}
        <Section>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 lg:gap-12">
            <Stat value="2,147+" label="Active Businesses" />
            <Stat value="4.2M" label="Messages Handled" />
            <Stat value="91%" label="Auto-Resolution Rate" />
            <Stat value="< 2s" label="Average Response" />
          </div>
        </Section>

        {/* ─────── Features ─────── */}
        <Section id="features" dark>
          <motion.div variants={fadeUp} className="text-center mb-16">
            <span className="badge-blue mb-4 inline-block">Features</span>
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
              Everything you need to automate support
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              From a simple chat widget to deep analytics, AutoReplyAI gives your team superpowers.
            </p>
          </motion.div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
            <FeatureCard
              icon={
                <svg className="w-6 h-6 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
                </svg>
              }
              title="Smart Chat Widget"
              description="AI-powered conversations that understand context, learn from your knowledge base, and resolve issues in real time."
            />
            <FeatureCard
              icon={
                <svg className="w-6 h-6 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
                </svg>
              }
              title="Knowledge Base"
              description="Train your AI on FAQs, docs, and product info. Drag to reorder priorities, bulk import from CSV."
            />
            <FeatureCard
              icon={
                <svg className="w-6 h-6 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
                </svg>
              }
              title="Real-Time Analytics"
              description="Track conversations, response times, satisfaction scores, and message volume with interactive charts."
            />
            <FeatureCard
              icon={
                <svg className="w-6 h-6 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9.53 16.122a3 3 0 00-5.78 1.128 2.25 2.25 0 01-2.4 2.245 4.5 4.5 0 008.4-2.245c0-.399-.078-.78-.22-1.128zm0 0a15.998 15.998 0 003.388-1.62m-5.043-.025a15.994 15.994 0 011.622-3.395m3.42 3.42a15.995 15.995 0 004.764-4.648l3.876-5.814a1.151 1.151 0 00-1.597-1.597L14.146 6.32a15.996 15.996 0 00-4.649 4.763m3.42 3.42a6.776 6.776 0 00-3.42-3.42" />
                </svg>
              }
              title="Widget Customization"
              description="Match your brand with custom colors, positioning, greeting messages, and a live preview editor."
            />
            <FeatureCard
              icon={
                <svg className="w-6 h-6 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
                </svg>
              }
              title="Stripe Billing"
              description="Built-in subscription management with Stripe. Upgrade, downgrade, or cancel with a click."
            />
            <FeatureCard
              icon={
                <svg className="w-6 h-6 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M14.25 9.75L16.5 12l-2.25 2.25m-4.5 0L7.5 12l2.25-2.25M6 20.25h12A2.25 2.25 0 0020.25 18V6A2.25 2.25 0 0018 3.75H6A2.25 2.25 0 003.75 6v12A2.25 2.25 0 006 20.25z" />
                </svg>
              }
              title="One-Line Install"
              description="Add a single script tag to your site. Works with any platform: React, WordPress, Shopify, or plain HTML."
            />
          </div>
        </Section>

        {/* ─────── Pricing ─────── */}
        <Section id="pricing">
          <motion.div variants={fadeUp} className="text-center mb-16">
            <span className="badge-blue mb-4 inline-block">Pricing</span>
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
              Start free, scale as you grow
            </h2>
            <p className="text-gray-400 max-w-xl mx-auto">
              No credit card required. Upgrade when you are ready.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            <PricingCard
              name="Free"
              price="$0"
              period="/month"
              description="For personal projects and testing"
              features={[
                '100 messages per month',
                'Basic AI responses',
                'Single widget',
                'Community support',
                '7-day conversation history',
              ]}
              cta="Get Started Free"
            />
            <PricingCard
              name="Pro"
              price="$19"
              period="/month"
              description="For growing businesses"
              features={[
                '5,000 messages per month',
                'Advanced AI with knowledge base',
                'Full analytics dashboard',
                'Widget customization',
                'Email support',
                'Unlimited conversation history',
              ]}
              cta="Start Pro Trial"
              featured
            />
            <PricingCard
              name="Business"
              price="$49"
              period="/month"
              description="For high-volume teams"
              features={[
                'Unlimited messages',
                'Priority AI processing',
                'Full analytics suite',
                'Custom branding',
                'Priority support',
                'API access',
                'Dedicated account manager',
              ]}
              cta="Start Business Trial"
            />
          </div>
        </Section>

        {/* ─────── Testimonials ─────── */}
        <Section id="testimonials" dark>
          <motion.div variants={fadeUp} className="text-center mb-16">
            <span className="badge-blue mb-4 inline-block">Testimonials</span>
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
              Loved by support teams everywhere
            </h2>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-5 max-w-5xl mx-auto">
            <TestimonialCard
              quote="AutoReplyAI cut our first-response time from 4 hours to under 2 seconds. Our CSAT score went from 3.2 to 4.8 in the first month."
              name="Sarah Chen"
              role="Head of Support, TechStart"
              initials="SC"
            />
            <TestimonialCard
              quote="Setup was incredibly fast. We imported our FAQ, customized the widget, and had it live on our Shopify store within 10 minutes."
              name="Marcus Rivera"
              role="Founder, EcoStore"
              initials="MR"
            />
            <TestimonialCard
              quote="We were spending $8k/month on live chat agents. AutoReplyAI handles 90% of queries now, saving us over $7k monthly."
              name="Emily Park"
              role="COO, FitnessPro"
              initials="EP"
            />
          </div>
        </Section>

        {/* ─────── FAQ ─────── */}
        <Section id="faq">
          <motion.div variants={fadeUp} className="text-center mb-16">
            <span className="badge-blue mb-4 inline-block">FAQ</span>
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
              Frequently asked questions
            </h2>
          </motion.div>

          <div className="max-w-2xl mx-auto">
            <FAQItem
              question="How does the AI know about my business?"
              answer="You train it through the Knowledge Base. Add FAQs, product info, policies, and any other content. The AI uses this to generate accurate, contextual responses specific to your business."
            />
            <FAQItem
              question="How long does setup take?"
              answer="Under 5 minutes. Register your site, add your knowledge base content, copy a single line of code to your website, and you're live. No coding experience needed."
            />
            <FAQItem
              question="What happens when the AI can't answer a question?"
              answer="The AI will honestly tell the visitor it doesn't have enough information and suggest they contact your support team directly. It never makes up answers."
            />
            <FAQItem
              question="Can I customize the widget's appearance?"
              answer="Absolutely. Change colors, position, greeting messages, and more from the dashboard. The live preview shows exactly how it will look on your site."
            />
            <FAQItem
              question="What AI model powers the responses?"
              answer="We use Google Gemini as the primary model with automatic fallback to ensure 99.9% uptime. Business plans support custom model configuration."
            />
            <FAQItem
              question="Can I cancel anytime?"
              answer="Yes, all plans are month-to-month with no contracts. Cancel from the billing dashboard and your plan will remain active until the end of the billing period."
            />
          </div>
        </Section>

        {/* ─────── CTA ─────── */}
        <section className="relative py-24 lg:py-32">
          <div className="absolute inset-0 bg-gradient-to-t from-brand-500/10 via-brand-500/5 to-transparent" />
          <div className="relative max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <motion.div
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={staggerContainer}
            >
              <motion.h2 variants={fadeUp} className="text-3xl lg:text-4xl font-bold text-white mb-4">
                Ready to automate your support?
              </motion.h2>
              <motion.p variants={fadeUp} className="text-gray-400 mb-8 text-lg">
                Join 2,000+ businesses using AutoReplyAI to deliver instant, accurate support 24/7.
              </motion.p>
              <motion.div variants={fadeUp}>
                <Link
                  href="/signup"
                  className="btn-primary px-8 py-3.5 text-base shadow-lg shadow-brand-500/25"
                >
                  Get Started Free
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </Link>
              </motion.div>
            </motion.div>
          </div>
        </section>
      </main>

      {/* ─────── Footer ─────── */}
      <footer className="bg-surface-500 border-t border-white/[0.04]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="col-span-2 md:col-span-1">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-7 h-7 rounded-lg bg-brand-500 flex items-center justify-center">
                  <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <span className="text-sm font-bold text-white">
                  AutoReply<span className="text-brand-400">AI</span>
                </span>
              </div>
              <p className="text-xs text-gray-500 leading-relaxed">
                AI-powered customer support that works around the clock.
              </p>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-4">Product</h4>
              <ul className="space-y-2.5">
                <li><a href="#features" className="text-sm text-gray-500 hover:text-gray-300 transition-colors">Features</a></li>
                <li><a href="#pricing" className="text-sm text-gray-500 hover:text-gray-300 transition-colors">Pricing</a></li>
                <li><Link href="/dashboard" className="text-sm text-gray-500 hover:text-gray-300 transition-colors">Dashboard</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-4">Company</h4>
              <ul className="space-y-2.5">
                <li><a href="/about" className="text-sm text-gray-500 hover:text-gray-300 transition-colors">About</a></li>
                <li><a href="/blog" className="text-sm text-gray-500 hover:text-gray-300 transition-colors">Blog</a></li>
                <li><a href="/careers" className="text-sm text-gray-500 hover:text-gray-300 transition-colors">Careers</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider mb-4">Legal</h4>
              <ul className="space-y-2.5">
                <li><a href="/privacy" className="text-sm text-gray-500 hover:text-gray-300 transition-colors">Privacy</a></li>
                <li><a href="/terms" className="text-sm text-gray-500 hover:text-gray-300 transition-colors">Terms</a></li>
                <li><a href="/gdpr" className="text-sm text-gray-500 hover:text-gray-300 transition-colors">GDPR</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-10 pt-6 border-t border-white/[0.04] text-center">
            <p className="text-xs text-gray-600">&copy; {new Date().getFullYear()} AutoReplyAI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </>
  );
}

/**
 * PRINTMAXX Universal Paywall Framework v1.0
 * Drop-in 7-day free trial + hard paywall for any PWA
 *
 * Usage:
 *   <script src="paywall.js"></script>
 *   <script>
 *     const pw = Paywall.init({
 *       appId: 'soberstreak',
 *       appName: 'SoberStreak',
 *       trialDays: 7,
 *       annualUrl: 'https://buy.stripe.com/...',
 *       monthlyUrl: 'https://buy.stripe.com/...',
 *       annualPrice: '$19.99/yr',
 *       monthlyPrice: '$2.99/mo',
 *       annualLabel: 'Best value — save 44%',
 *       features: ['Track 5 habits', 'Data export', 'Custom milestones'],
 *       premiumFeatures: ['multi-habit', 'export', 'custom-milestones'],
 *       reviewUrl: 'https://soberstreak.surge.sh/',
 *       reviewMilestones: [7, 30, 90, 365],
 *     });
 *   </script>
 *
 * API:
 *   pw.isPremium()           -> boolean
 *   pw.trialDaysLeft()       -> number (0 if expired)
 *   pw.isTrialActive()       -> boolean
 *   pw.gate('feature-name')  -> boolean (true = allow, false = paywall shown)
 *   pw.showModal()           -> void
 *   pw.markMilestone(n)      -> void (triggers review prompt if milestone hit)
 *   pw.activatePremium()     -> void (call after Stripe success confirmation)
 *   pw.onUpgrade(fn)         -> void (callback when user clicks a payment link)
 */

(function (global) {
  'use strict';

  // ── Safe URL validation ─────────────────────────────────────────────────
  function safeUrl(url) {
    try {
      const u = new URL(url);
      return (u.protocol === 'https:') ? url : '#';
    } catch (e) { return '#'; }
  }

  // ── Safe text node helper ───────────────────────────────────────────────
  function txt(str) { return document.createTextNode(String(str || '')); }

  function el(tag, props, children) {
    const node = document.createElement(tag);
    if (props) {
      Object.entries(props).forEach(([k, v]) => {
        if (k === 'style') { node.style.cssText = v; }
        else if (k === 'className') { node.className = v; }
        else if (k === 'id') { node.id = v; }
        else if (k === 'href') { node.href = safeUrl(v); }
        else if (k === 'target' || k === 'rel') { node.setAttribute(k, v); }
        else if (k.startsWith('on') && typeof v === 'function') {
          node.addEventListener(k.slice(2), v);
        }
      });
    }
    (children || []).forEach(child => {
      if (child == null) return;
      node.appendChild(typeof child === 'string' ? txt(child) : child);
    });
    return node;
  }

  // ── Persistence ─────────────────────────────────────────────────────────
  function storeKey(appId, suffix) { return 'pw_' + appId + '_' + suffix; }
  function load(appId, suffix, def) {
    try { return JSON.parse(localStorage.getItem(storeKey(appId, suffix))) ?? def; }
    catch (e) { return def; }
  }
  function save(appId, suffix, val) {
    try { localStorage.setItem(storeKey(appId, suffix), JSON.stringify(val)); } catch (e) {}
  }

  // ── CSS (injected once) ─────────────────────────────────────────────────
  function injectStyles() {
    if (document.getElementById('pw-styles')) return;
    const s = document.createElement('style');
    s.id = 'pw-styles';
    s.textContent = `
      .pw-overlay{position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.88);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;padding:1.5rem;animation:pw-fi .2s ease}
      @keyframes pw-fi{from{opacity:0}to{opacity:1}}
      .pw-box{width:100%;max-width:420px;border-radius:1.5rem;padding:1.75rem;position:relative;background:#1a1a2e;border:1px solid rgba(255,255,255,.1);animation:pw-su .25s cubic-bezier(.4,0,.2,1)}
      @keyframes pw-su{from{transform:translateY(20px);opacity:0}to{transform:translateY(0);opacity:1}}
      .pw-close{position:absolute;top:1rem;right:1rem;background:none;border:none;color:#9ca3af;font-size:1.25rem;cursor:pointer;line-height:1;padding:.25rem .5rem;border-radius:.5rem}
      .pw-close:hover{color:#fff}
      .pw-icon{font-size:2.5rem;text-align:center;margin-bottom:.5rem}
      .pw-title{font-size:1.25rem;font-weight:800;color:#fff;text-align:center;margin-bottom:.25rem}
      .pw-sub{font-size:.875rem;color:#9ca3af;text-align:center;margin-bottom:1.25rem}
      .pw-trial-bar{display:flex;align-items:center;gap:.5rem;padding:.625rem .875rem;border-radius:.75rem;margin-bottom:1rem;background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.2)}
      .pw-trial-text{font-size:.8125rem;color:#fbbf24;flex:1}
      .pw-card{border-radius:.875rem;padding:.875rem 1rem;margin-bottom:.75rem;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08)}
      .pw-card-featured{border-color:rgba(124,58,237,.5);background:rgba(109,40,217,.12)}
      .pw-card-row{display:flex;justify-content:space-between;align-items:center}
      .pw-plan-name{color:#fff;font-weight:700;font-size:.9375rem}
      .pw-plan-note{color:#9ca3af;font-size:.75rem;margin-top:.125rem}
      .pw-price{color:#a78bfa;font-weight:900;font-size:1.25rem;text-align:right}
      .pw-price-dim{color:#d1d5db;font-weight:700;font-size:1.0625rem;text-align:right}
      .pw-price-sub{color:#9ca3af;font-size:.75rem}
      .pw-badge{display:inline-block;background:#7c3aed;color:#fff;font-size:.6875rem;font-weight:700;padding:.125rem .5rem;border-radius:999px;margin-top:.375rem}
      .pw-feature-list{margin-bottom:1rem}
      .pw-feature{font-size:.8125rem;color:#d1d5db;padding:.25rem 0;display:flex;gap:.5rem}
      .pw-feature-check{color:#7c3aed;font-weight:700;flex-shrink:0}
      .pw-btn-primary{display:block;width:100%;padding:.875rem;border-radius:.875rem;font-weight:800;font-size:.9375rem;color:#fff;text-align:center;text-decoration:none;background:linear-gradient(135deg,#6d28d9,#7c3aed);border:none;cursor:pointer;margin-bottom:.625rem;transition:opacity .15s}
      .pw-btn-primary:hover{opacity:.9}
      .pw-btn-secondary{display:block;width:100%;padding:.625rem;border-radius:.875rem;font-size:.875rem;color:#9ca3af;text-align:center;text-decoration:none;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);cursor:pointer;transition:color .15s;margin-bottom:.625rem}
      .pw-btn-secondary:hover{color:#d1d5db}
      .pw-footer-text{color:#6b7280;font-size:.75rem;text-align:center;margin-top:.75rem}
      .pw-review-box{width:100%;max-width:380px;border-radius:1.5rem;padding:1.75rem;background:#1a1a2e;border:1px solid rgba(124,58,237,.3);animation:pw-su .25s ease;text-align:center}
      .pw-review-icon{font-size:3rem;margin-bottom:.75rem}
      .pw-review-title{font-size:1.25rem;font-weight:800;color:#fff;margin-bottom:.5rem}
      .pw-review-body{font-size:.875rem;color:#9ca3af;line-height:1.5;margin-bottom:1.25rem}
      .pw-review-yes{display:block;width:100%;padding:.875rem;border-radius:.875rem;font-weight:700;color:#fff;background:linear-gradient(135deg,#6d28d9,#7c3aed);border:none;cursor:pointer;margin-bottom:.5rem;font-size:.9375rem;text-decoration:none;text-align:center}
      .pw-review-later{display:block;width:100%;padding:.5rem;background:none;border:none;color:#6b7280;font-size:.875rem;cursor:pointer}
    `;
    document.head.appendChild(s);
  }

  // ── Trial logic ──────────────────────────────────────────────────────────
  function now() { return Date.now(); }
  function daysAgo(ts) { return Math.floor((now() - ts) / 86400000); }

  function _trialDaysLeft(cfg) {
    const start = load(cfg.appId, 'trial_start', null);
    if (!start) return cfg.trialDays; // not started yet
    return Math.max(0, cfg.trialDays - Math.floor((now() - start) / 86400000));
  }
  function _isTrialActive(cfg) {
    const start = load(cfg.appId, 'trial_start', null);
    return !!start && _trialDaysLeft(cfg) > 0;
  }
  function _isPremium(cfg) { return load(cfg.appId, 'premium', false) === true; }
  function _isAllowed(cfg) { return _isPremium(cfg) || _isTrialActive(cfg); }

  // ── Modal builders (DOM-safe) ────────────────────────────────────────────
  function buildPaywallModal(cfg, dismissible) {
    const overlay = el('div', { className: 'pw-overlay' });
    const box = el('div', { className: 'pw-box' });

    if (dismissible) {
      const closeBtn = el('button', { className: 'pw-close', 'onclick': () => overlay.remove() }, ['✕']);
      box.appendChild(closeBtn);
    }

    box.appendChild(el('div', { className: 'pw-icon' }, [cfg.icon || '🔓']));
    box.appendChild(el('div', { className: 'pw-title' }, [cfg.appName + ' Pro']));
    box.appendChild(el('div', { className: 'pw-sub' }, [cfg.tagline || 'Unlock all features']));

    const left = _trialDaysLeft(cfg);
    if (cfg.trialDays > 0 && left > 0) {
      const bar = el('div', { className: 'pw-trial-bar' });
      const span = el('span', { className: 'pw-trial-text' });
      span.appendChild(txt('⏳ Free trial: '));
      const strong = el('strong', {}, [left + ' day' + (left !== 1 ? 's' : '') + ' left']);
      span.appendChild(strong);
      span.appendChild(txt(' — upgrade before it ends'));
      bar.appendChild(span);
      box.appendChild(bar);
    }

    // Annual card
    const annualCard = el('div', { className: 'pw-card pw-card-featured' });
    const annualRow = el('div', { className: 'pw-card-row' });
    const annualLeft = el('div');
    annualLeft.appendChild(el('div', { className: 'pw-plan-name' }, ['Annual Plan']));
    annualLeft.appendChild(el('div', { className: 'pw-plan-note' }, [cfg.annualLabel || 'Best value']));
    const annualRight = el('div');
    annualRight.appendChild(el('div', { className: 'pw-price' }, [cfg.annualPrice]));
    annualRight.appendChild(el('div', { className: 'pw-price-sub' }, ['per year']));
    annualRow.appendChild(annualLeft);
    annualRow.appendChild(annualRight);
    annualCard.appendChild(annualRow);
    annualCard.appendChild(el('div', { className: 'pw-badge' }, ['BEST VALUE']));
    box.appendChild(annualCard);

    // Monthly card
    const monthlyCard = el('div', { className: 'pw-card' });
    const monthlyRow = el('div', { className: 'pw-card-row' });
    const monthlyLeft = el('div');
    monthlyLeft.appendChild(el('div', { className: 'pw-plan-name' }, ['Monthly Plan']));
    monthlyLeft.appendChild(el('div', { className: 'pw-plan-note' }, ['Cancel anytime']));
    const monthlyRight = el('div');
    monthlyRight.appendChild(el('div', { className: 'pw-price-dim' }, [cfg.monthlyPrice]));
    monthlyRight.appendChild(el('div', { className: 'pw-price-sub' }, ['per month']));
    monthlyRow.appendChild(monthlyLeft);
    monthlyRow.appendChild(monthlyRight);
    monthlyCard.appendChild(monthlyRow);
    box.appendChild(monthlyCard);

    // Features
    if (cfg.features && cfg.features.length) {
      const featureList = el('div', { className: 'pw-feature-list' });
      cfg.features.forEach(f => {
        const row = el('div', { className: 'pw-feature' });
        row.appendChild(el('span', { className: 'pw-feature-check' }, ['✓']));
        row.appendChild(txt(String(f)));
        featureList.appendChild(row);
      });
      box.appendChild(featureList);
    }

    // CTA buttons
    const annualBtn = el('a', {
      className: 'pw-btn-primary',
      href: cfg.annualUrl,
      target: '_blank',
      rel: 'noopener',
    }, ['Get Annual Plan — ' + cfg.annualPrice]);
    annualBtn.addEventListener('click', () => cfg._upgradeCallbacks.forEach(fn => fn()));
    box.appendChild(annualBtn);

    const monthlyBtn = el('a', {
      className: 'pw-btn-secondary',
      href: cfg.monthlyUrl,
      target: '_blank',
      rel: 'noopener',
    }, ['Monthly — ' + cfg.monthlyPrice]);
    monthlyBtn.addEventListener('click', () => cfg._upgradeCallbacks.forEach(fn => fn()));
    box.appendChild(monthlyBtn);

    box.appendChild(el('div', { className: 'pw-footer-text' }, ['Cancel anytime. Your data stays on your device.']));

    overlay.appendChild(box);

    if (dismissible) {
      overlay.addEventListener('click', e => { if (e.target === overlay) overlay.remove(); });
    }

    return overlay;
  }

  const REVIEW_MESSAGES = {
    7:   { icon: '💎', title: 'days. That\'s real.', body: 'Your consistency is working. If {appName} helped, a quick rating keeps it free for everyone.' },
    14:  { icon: '⚡', title: 'Two weeks strong.', body: 'Halfway to a month. If {appName} is part of your routine, a rating helps more people find it.' },
    30:  { icon: '🏆', title: 'One full month.', body: '30 days is elite consistency. If this app played a part, leave a quick review.' },
    90:  { icon: '🚀', title: 'Three months.', body: 'You\'re in the top 5% of people who start. If {appName} helped, share it.' },
    365: { icon: '🎯', title: 'One year.', body: 'An entire year. Thank you. A review means a lot.' },
  };

  function buildReviewModal(cfg, milestoneDays, onRate, onLater) {
    const msg = REVIEW_MESSAGES[milestoneDays] || {
      icon: '⭐', title: `${milestoneDays} days!`, body: 'Thanks for sticking with {appName}. A quick rating helps.',
    };

    const overlay = el('div', { className: 'pw-overlay' });
    const box = el('div', { className: 'pw-review-box' });

    box.appendChild(el('div', { className: 'pw-review-icon' }, [msg.icon]));

    const title = milestoneDays in REVIEW_MESSAGES && milestoneDays === 7
      ? `${milestoneDays} ${msg.title}` : msg.title;
    box.appendChild(el('div', { className: 'pw-review-title' }, [title]));
    box.appendChild(el('div', { className: 'pw-review-body' }, [msg.body.replace('{appName}', cfg.appName)]));

    const rateBtn = el('a', {
      className: 'pw-review-yes',
      href: cfg.reviewUrl,
      target: '_blank',
      rel: 'noopener',
    }, ['Rate ' + cfg.appName + ' ⭐⭐⭐⭐⭐']);
    rateBtn.addEventListener('click', () => { onRate(); overlay.remove(); });
    box.appendChild(rateBtn);

    const laterBtn = el('button', { className: 'pw-review-later', 'onclick': () => { onLater(); overlay.remove(); } }, ['Maybe later']);
    box.appendChild(laterBtn);

    overlay.appendChild(box);
    return overlay;
  }

  // ── Review prompt logic ──────────────────────────────────────────────────
  function maybeShowReview(cfg, milestoneDays) {
    const COOLDOWN = 90;
    const lastReview = load(cfg.appId, 'last_review', null);
    if (lastReview && daysAgo(lastReview) < COOLDOWN) return;

    const shown = load(cfg.appId, 'review_milestones', []);
    if (shown.includes(milestoneDays)) return;

    setTimeout(() => {
      injectStyles();
      const existing = document.querySelector('.pw-overlay');
      if (existing) return; // don't stack modals

      const onRate = () => {
        save(cfg.appId, 'last_review', now());
        save(cfg.appId, 'review_milestones', [...shown, milestoneDays]);
      };
      const onLater = () => {
        save(cfg.appId, 'review_milestones', [...shown, milestoneDays]);
      };

      document.body.appendChild(buildReviewModal(cfg, milestoneDays, onRate, onLater));
    }, 1200);
  }

  // ── init ─────────────────────────────────────────────────────────────────
  function init(userCfg) {
    if (!userCfg || !userCfg.appId) throw new Error('Paywall.init: appId is required');
    if (!userCfg.annualUrl || !userCfg.monthlyUrl) throw new Error('Paywall.init: annualUrl and monthlyUrl are required');

    const cfg = Object.assign({
      trialDays: 7,
      icon: '🔓',
      tagline: 'Unlock all features',
      annualLabel: 'Best value',
      features: [],
      premiumFeatures: [],
      reviewUrl: window.location.href,
      reviewMilestones: [7, 30, 90, 365],
      _upgradeCallbacks: [],
    }, userCfg);

    // Start trial on first ever visit
    if (!load(cfg.appId, 'trial_start', null)) {
      save(cfg.appId, 'trial_start', now());
    }

    return {
      isPremium: () => _isPremium(cfg),
      trialDaysLeft: () => _trialDaysLeft(cfg),
      isTrialActive: () => _isTrialActive(cfg),
      isAllowed: () => _isAllowed(cfg),
      /**
       * Gate a premium feature by name.
       * Returns true if user is allowed, false + shows paywall if not.
       */
      gate(featureName) {
        if (!featureName || !cfg.premiumFeatures.includes(featureName)) return true;
        if (_isAllowed(cfg)) return true;
        this.showModal();
        return false;
      },
      showModal(dismissible = true) {
        injectStyles();
        const existing = document.querySelector('.pw-overlay');
        if (existing) existing.remove();
        document.body.appendChild(buildPaywallModal(cfg, dismissible));
      },
      /** Call when user reaches a numerical milestone (streak day, session count, etc.) */
      markMilestone(n) {
        if (cfg.reviewMilestones.includes(n)) maybeShowReview(cfg, n);
      },
      onUpgrade(fn) { if (typeof fn === 'function') cfg._upgradeCallbacks.push(fn); },
      /** Call after your Stripe success redirect to unlock premium in localStorage. */
      activatePremium() { save(cfg.appId, 'premium', true); },
    };
  }

  global.Paywall = { init };
})(window);

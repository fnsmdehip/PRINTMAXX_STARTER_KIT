/**
 * PRINTMAXX Universal Lead Capture
 * ==================================
 * Drop this into any surge.sh page to capture emails.
 *
 * Usage (in any HTML page):
 *   <script src="lead-capture-universal.js"></script>
 *
 *   Add a form with id="lead-form" and an email input:
 *   <form id="lead-form">
 *     <input type="email" name="email" placeholder="your@email.com" required />
 *     <button type="submit">Get free access</button>
 *   </form>
 *
 *   Optional overrides (set BEFORE loading this script):
 *   <script>
 *     window.LEAD_ENDPOINT = 'https://your-server.com/lead';
 *     window.LEAD_SOURCE   = 'cold-email-calculator';
 *   </script>
 *
 * What it does:
 *   1. Parses UTM params from the URL
 *   2. On submit: POSTs to endpoint + saves to localStorage as backup
 *   3. Shows a "thank you" modal on success
 *   4. Records source URL so we know which page sent each lead
 *   5. Auto-flushes localStorage backup when server comes back online
 */

(function () {
  'use strict';

  // -------------------------------------------------------------------------
  // Config — override with window.LEAD_ENDPOINT / window.LEAD_SOURCE
  // -------------------------------------------------------------------------
  var ENDPOINT = window.LEAD_ENDPOINT || 'https://formsubmit.co/ajax/printmaxxweb@gmail.com';
  var SOURCE   = window.LEAD_SOURCE   || location.hostname + location.pathname;

  // -------------------------------------------------------------------------
  // UTM parsing
  // -------------------------------------------------------------------------
  function parseUtms() {
    var params = new URLSearchParams(location.search);
    return {
      utm_source:   params.get('utm_source')   || '',
      utm_medium:   params.get('utm_medium')   || '',
      utm_campaign: params.get('utm_campaign') || '',
      utm_content:  params.get('utm_content')  || '',
      utm_term:     params.get('utm_term')     || ''
    };
  }

  // -------------------------------------------------------------------------
  // localStorage backup — survives server downtime
  // -------------------------------------------------------------------------
  function backupToStorage(payload) {
    try {
      var key = 'pm_leads_pending';
      var existing = JSON.parse(localStorage.getItem(key) || '[]');
      existing.push(payload);
      localStorage.setItem(key, JSON.stringify(existing));
    } catch (e) { /* storage may be blocked in some browsers — non-fatal */ }
  }

  // Flush pending local backups when the server is reachable
  function flushPending() {
    try {
      var key = 'pm_leads_pending';
      var pending = JSON.parse(localStorage.getItem(key) || '[]');
      if (!pending.length) return;

      var remaining = [];
      var sent = 0;

      pending.forEach(function (payload) {
        fetch(ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }).then(function (r) {
          if (!r.ok) remaining.push(payload);
          else sent++;
        }).catch(function () {
          remaining.push(payload);
        });
      });

      // Give in-flight requests 4s to resolve before writing back
      setTimeout(function () {
        localStorage.setItem(key, JSON.stringify(remaining));
      }, 4000);
    } catch (e) { /* ignore */ }
  }

  // -------------------------------------------------------------------------
  // Thank-you modal — built with DOM methods to avoid innerHTML risks
  // -------------------------------------------------------------------------
  function showModal(email) {
    var overlay = document.createElement('div');
    overlay.id = 'pm-modal-overlay';
    overlay.style.cssText = [
      'position:fixed', 'inset:0', 'background:rgba(0,0,0,0.65)',
      'display:flex', 'align-items:center', 'justify-content:center',
      'z-index:99999', 'font-family:system-ui,sans-serif'
    ].join(';');

    var box = document.createElement('div');
    box.style.cssText = [
      'background:#fff', 'border-radius:12px', 'padding:40px 36px',
      'max-width:420px', 'width:90%', 'text-align:center',
      'box-shadow:0 20px 60px rgba(0,0,0,0.3)'
    ].join(';');

    var icon = document.createElement('div');
    icon.textContent = '\u2714';
    icon.style.cssText = 'font-size:40px;margin-bottom:12px;color:#16a34a';

    var heading = document.createElement('h2');
    heading.textContent = "You're in.";
    heading.style.cssText = 'margin:0 0 10px;font-size:22px;font-weight:700;color:#111';

    var desc = document.createElement('p');
    desc.style.cssText = 'margin:0 0 24px;color:#555;font-size:15px;line-height:1.5';
    desc.textContent = 'Sent to ';

    var emailSpan = document.createElement('strong');
    emailSpan.textContent = email; // textContent — XSS-safe
    desc.appendChild(emailSpan);

    var lineBreak = document.createElement('br');
    desc.appendChild(lineBreak);

    var desc2 = document.createTextNode('Check your inbox in the next few minutes.');
    desc.appendChild(desc2);

    var closeBtn = document.createElement('button');
    closeBtn.textContent = 'Close';
    closeBtn.style.cssText = [
      'background:#111', 'color:#fff', 'border:none', 'border-radius:8px',
      'padding:12px 28px', 'font-size:15px', 'font-weight:600', 'cursor:pointer', 'width:100%'
    ].join(';');

    box.appendChild(icon);
    box.appendChild(heading);
    box.appendChild(desc);
    box.appendChild(closeBtn);
    overlay.appendChild(box);
    document.body.appendChild(overlay);

    closeBtn.addEventListener('click', function () { overlay.remove(); });
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) overlay.remove();
    });
  }

  // -------------------------------------------------------------------------
  // Wire up a single form element
  // -------------------------------------------------------------------------
  function wireForm(form) {
    // Avoid double-wiring
    if (form._pmWired) return;
    form._pmWired = true;

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var emailInput = form.querySelector('input[name="email"], input[type="email"]');
      if (!emailInput) return;

      var email = (emailInput.value || '').trim();
      if (!email || email.indexOf('@') === -1) {
        emailInput.style.outline = '2px solid #e00';
        emailInput.focus();
        return;
      }
      emailInput.style.outline = '';

      var utms = parseUtms();
      var payload = {
        email:        email,
        source:       SOURCE,
        page_url:     location.href,
        referrer:     document.referrer || '',
        utm_source:   utms.utm_source,
        utm_medium:   utms.utm_medium,
        utm_campaign: utms.utm_campaign,
        utm_content:  utms.utm_content,
        utm_term:     utms.utm_term,
        captured_at:  new Date().toISOString()
      };

      // Save to localStorage immediately — server may be offline
      backupToStorage(payload);

      // Submit button feedback
      var btn = form.querySelector('button[type="submit"], input[type="submit"], button:not([type])');
      var originalText = btn ? (btn.textContent || btn.value || 'Submit') : '';
      if (btn) {
        btn.disabled = true;
        if (btn.tagName === 'BUTTON') btn.textContent = 'Sending...';
        else btn.value = 'Sending...';
      }

      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .catch(function () {
          // Server unreachable — lead is already in localStorage, show success anyway
          return { ok: false };
        })
        .then(function () {
          showModal(email);
          form.reset();
          if (btn) {
            btn.disabled = false;
            if (btn.tagName === 'BUTTON') btn.textContent = originalText;
            else btn.value = originalText;
          }
        });
    });
  }

  // -------------------------------------------------------------------------
  // Init
  // -------------------------------------------------------------------------
  function init() {
    flushPending();

    // Wire existing forms
    var forms = document.querySelectorAll('#lead-form, .lead-form, [data-lead-form]');
    for (var i = 0; i < forms.length; i++) {
      wireForm(forms[i]);
    }

    // Watch for dynamically inserted forms (SPAs, lazy sections)
    if (typeof MutationObserver !== 'undefined') {
      var observer = new MutationObserver(function (mutations) {
        for (var mi = 0; mi < mutations.length; mi++) {
          var added = mutations[mi].addedNodes;
          for (var ni = 0; ni < added.length; ni++) {
            var node = added[ni];
            if (node.nodeType !== 1) continue;
            if (node.matches && node.matches('#lead-form, .lead-form, [data-lead-form]')) {
              wireForm(node);
            }
            if (node.querySelectorAll) {
              var nested = node.querySelectorAll('#lead-form, .lead-form, [data-lead-form]');
              for (var fi = 0; fi < nested.length; fi++) wireForm(nested[fi]);
            }
          }
        }
      });
      observer.observe(document.body, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();

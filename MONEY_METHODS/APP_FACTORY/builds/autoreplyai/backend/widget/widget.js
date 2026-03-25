/**
 * AutoReplyAI Embeddable Widget
 * Usage: <script src="https://your-domain.com/widget/widget.js" data-key="arai_xxx"></script>
 * Options (data attributes):
 *   data-key       - Required. Your API key.
 *   data-color     - Primary color (default: from server settings).
 *   data-position  - bottom-right | bottom-left (default: from server settings).
 *   data-greeting  - Custom greeting message.
 */
(function () {
  'use strict';

  // --- Config from script tag ---
  var scriptTag = document.currentScript || (function () {
    var scripts = document.getElementsByTagName('script');
    for (var i = scripts.length - 1; i >= 0; i--) {
      if (scripts[i].src && scripts[i].src.indexOf('widget.js') !== -1) return scripts[i];
    }
    return null;
  })();

  var API_KEY = scriptTag ? scriptTag.getAttribute('data-key') : null;
  var OVERRIDE_COLOR = scriptTag ? scriptTag.getAttribute('data-color') : null;
  var OVERRIDE_POSITION = scriptTag ? scriptTag.getAttribute('data-position') : null;
  var OVERRIDE_GREETING = scriptTag ? scriptTag.getAttribute('data-greeting') : null;

  if (!API_KEY) {
    console.error('AutoReplyAI: data-key attribute is required on the script tag.');
    return;
  }

  // Determine API base URL from script src
  var API_BASE = (function () {
    if (scriptTag && scriptTag.src) {
      try {
        var url = new URL(scriptTag.src);
        return url.origin;
      } catch (e) {
        return 'http://localhost:3001';
      }
    }
    return 'http://localhost:3001';
  })();

  // --- State ---
  var state = {
    isOpen: false,
    isLoading: false,
    conversationId: null,
    settings: {
      primaryColor: OVERRIDE_COLOR || '#4f46e5',
      position: OVERRIDE_POSITION || 'bottom-right',
      greeting: OVERRIDE_GREETING || 'Hi! How can I help you today?',
      name: 'Support',
    },
    messages: [],
  };

  // --- Styles ---
  var WIDGET_ID = 'autoreplyai-widget-root';

  function injectStyles() {
    if (document.getElementById('autoreplyai-styles')) return;
    var style = document.createElement('style');
    style.id = 'autoreplyai-styles';
    style.textContent = [
      '#' + WIDGET_ID + ' { position:fixed; z-index:2147483647; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; font-size:14px; line-height:1.5; }',
      '#' + WIDGET_ID + ' * { box-sizing:border-box; margin:0; padding:0; }',
      '.arai-btn { width:60px; height:60px; border-radius:50%; border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; transition:transform .2s,box-shadow .2s; box-shadow:0 4px 16px rgba(0,0,0,.2); }',
      '.arai-btn:hover { transform:scale(1.1); box-shadow:0 6px 24px rgba(0,0,0,.3); }',
      '.arai-btn svg { width:28px; height:28px; fill:#fff; }',
      '.arai-window { position:absolute; width:380px; max-width:calc(100vw - 32px); height:520px; max-height:calc(100vh - 100px); background:#fff; border-radius:16px; box-shadow:0 12px 40px rgba(0,0,0,.2); display:none; flex-direction:column; overflow:hidden; }',
      '.arai-window.open { display:flex; }',
      '.arai-header { padding:16px 20px; color:#fff; display:flex; align-items:center; justify-content:space-between; flex-shrink:0; }',
      '.arai-header-title { font-size:16px; font-weight:600; }',
      '.arai-header button { background:none; border:none; color:#fff; cursor:pointer; opacity:.8; transition:opacity .2s; font-size:20px; line-height:1; }',
      '.arai-header button:hover { opacity:1; }',
      '.arai-messages { flex:1; overflow-y:auto; padding:16px; display:flex; flex-direction:column; gap:10px; background:#f9fafb; }',
      '.arai-msg { max-width:85%; padding:10px 14px; border-radius:16px; font-size:14px; word-wrap:break-word; animation:araiSlideIn .2s ease; }',
      '.arai-msg-user { align-self:flex-end; color:#fff; border-bottom-right-radius:4px; }',
      '.arai-msg-bot { align-self:flex-start; background:#f3f4f6; color:#1f2937; border-bottom-left-radius:4px; }',
      '.arai-input-area { display:flex; padding:12px 16px; border-top:1px solid #e5e7eb; background:#fff; gap:8px; flex-shrink:0; }',
      '.arai-input { flex:1; padding:10px 16px; border:1px solid #d1d5db; border-radius:24px; outline:none; font-size:14px; transition:border-color .2s; }',
      '.arai-send { width:40px; height:40px; border-radius:50%; border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; color:#fff; transition:opacity .2s; }',
      '.arai-send:disabled { opacity:.5; cursor:default; }',
      '.arai-send svg { width:18px; height:18px; fill:#fff; }',
      '.arai-typing { display:flex; gap:4px; padding:4px 0; align-self:flex-start; }',
      '.arai-typing span { width:8px; height:8px; background:#9ca3af; border-radius:50%; animation:araiBounce .6s infinite alternate; }',
      '.arai-typing span:nth-child(2) { animation-delay:.2s; }',
      '.arai-typing span:nth-child(3) { animation-delay:.4s; }',
      '.arai-powered { text-align:center; padding:6px; font-size:11px; color:#9ca3af; background:#fff; border-top:1px solid #f3f4f6; flex-shrink:0; }',
      '.arai-powered a { color:#6366f1; text-decoration:none; }',
      '@keyframes araiSlideIn { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }',
      '@keyframes araiBounce { to { transform:translateY(-4px); } }',
      '@media (max-width:480px) { .arai-window { width:100vw; height:100vh; max-height:100vh; border-radius:0; position:fixed; top:0; left:0; right:0; bottom:0; } }',
    ].join('\n');
    document.head.appendChild(style);
  }

  // Safe text-setting helper (no innerHTML)
  function setText(el, text) {
    el.textContent = text;
  }

  // Create an SVG element safely (no innerHTML)
  function createSvgIcon(pathD, size) {
    var ns = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('width', size || '24');
    svg.setAttribute('height', size || '24');
    var path = document.createElementNS(ns, 'path');
    path.setAttribute('d', pathD);
    path.setAttribute('fill', '#fff');
    svg.appendChild(path);
    return svg;
  }

  // --- DOM Construction ---
  function buildWidget() {
    injectStyles();

    var root = document.createElement('div');
    root.id = WIDGET_ID;
    var pos = state.settings.position;
    var isRight = pos !== 'bottom-left';
    root.style.cssText = 'bottom:20px;' + (isRight ? 'right:20px;' : 'left:20px;');

    // Chat window
    var win = document.createElement('div');
    win.className = 'arai-window';
    win.style.cssText = 'bottom:72px;' + (isRight ? 'right:0;' : 'left:0;');
    win.id = 'arai-window';

    // Header
    var header = document.createElement('div');
    header.className = 'arai-header';
    header.style.background = state.settings.primaryColor;

    var headerTitle = document.createElement('span');
    headerTitle.className = 'arai-header-title';
    headerTitle.id = 'arai-header-title';
    setText(headerTitle, state.settings.name);

    var closeBtn = document.createElement('button');
    closeBtn.id = 'arai-close';
    closeBtn.setAttribute('aria-label', 'Close chat');
    setText(closeBtn, '\u00D7'); // multiplication sign as close icon

    header.appendChild(headerTitle);
    header.appendChild(closeBtn);

    // Messages
    var messagesEl = document.createElement('div');
    messagesEl.className = 'arai-messages';
    messagesEl.id = 'arai-messages';

    // Input area
    var inputArea = document.createElement('div');
    inputArea.className = 'arai-input-area';

    var input = document.createElement('input');
    input.className = 'arai-input';
    input.id = 'arai-input';
    input.type = 'text';
    input.placeholder = 'Type your message...';
    input.setAttribute('aria-label', 'Type your message');

    var sendBtn = document.createElement('button');
    sendBtn.className = 'arai-send';
    sendBtn.id = 'arai-send';
    sendBtn.style.background = state.settings.primaryColor;
    sendBtn.setAttribute('aria-label', 'Send message');
    sendBtn.appendChild(createSvgIcon('M2.01 21L23 12 2.01 3 2 10l15 2-15 2z', '18'));

    inputArea.appendChild(input);
    inputArea.appendChild(sendBtn);

    // Powered by
    var powered = document.createElement('div');
    powered.className = 'arai-powered';
    var poweredText = document.createTextNode('Powered by ');
    var poweredLink = document.createElement('a');
    poweredLink.href = 'https://autoreplyai.com';
    poweredLink.target = '_blank';
    poweredLink.rel = 'noopener';
    setText(poweredLink, 'AutoReplyAI');
    powered.appendChild(poweredText);
    powered.appendChild(poweredLink);

    win.appendChild(header);
    win.appendChild(messagesEl);
    win.appendChild(inputArea);
    win.appendChild(powered);

    // Toggle button
    var btn = document.createElement('button');
    btn.className = 'arai-btn';
    btn.id = 'arai-toggle';
    btn.style.background = state.settings.primaryColor;
    btn.setAttribute('aria-label', 'Open chat');
    btn.appendChild(createSvgIcon('M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z', '28'));

    root.appendChild(win);
    root.appendChild(btn);
    document.body.appendChild(root);

    // --- Events ---
    btn.addEventListener('click', toggleWidget);
    closeBtn.addEventListener('click', toggleWidget);
    sendBtn.addEventListener('click', function () { sendMessage(); });
    input.addEventListener('keypress', function (e) { if (e.key === 'Enter') sendMessage(); });
  }

  function toggleWidget() {
    state.isOpen = !state.isOpen;
    var win = document.getElementById('arai-window');
    if (state.isOpen) {
      win.classList.add('open');
    } else {
      win.classList.remove('open');
    }

    if (state.isOpen && !state.conversationId) {
      initSession();
    }

    if (state.isOpen) {
      setTimeout(function () {
        var inp = document.getElementById('arai-input');
        if (inp) inp.focus();
      }, 100);
    }
  }

  // --- API Calls ---
  async function initSession() {
    try {
      var resp = await fetch(API_BASE + '/api/widget/init', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ apiKey: API_KEY }),
      });

      if (!resp.ok) throw new Error('Init failed');

      var data = await resp.json();
      state.conversationId = data.conversationId;

      // Apply server settings (unless overridden by data attributes)
      if (data.settings) {
        if (!OVERRIDE_COLOR && data.settings.primaryColor) {
          state.settings.primaryColor = data.settings.primaryColor;
          applyColor(data.settings.primaryColor);
        }
        if (data.settings.name) {
          state.settings.name = data.settings.name;
        }
        if (!OVERRIDE_GREETING && data.settings.greeting) {
          state.settings.greeting = data.settings.greeting;
        }
      }

      // Update header name safely
      var titleEl = document.getElementById('arai-header-title');
      if (titleEl) setText(titleEl, state.settings.name);

      // Show greeting
      addMessage(state.settings.greeting, 'bot');
    } catch (err) {
      console.error('AutoReplyAI init error:', err);
      addMessage('Sorry, we are having trouble connecting. Please try again later.', 'bot');
    }
  }

  async function sendMessage() {
    var input = document.getElementById('arai-input');
    var text = input.value.trim();
    if (!text || state.isLoading) return;

    input.value = '';
    addMessage(text, 'user');
    showTyping();
    state.isLoading = true;

    try {
      var resp = await fetch(API_BASE + '/api/widget/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversationId: state.conversationId,
          message: text,
          apiKey: API_KEY,
        }),
      });

      hideTyping();

      if (!resp.ok) {
        var errData = await resp.json().catch(function () { return {}; });
        throw new Error(errData.error || 'Request failed');
      }

      var data = await resp.json();
      addMessage(data.response, 'bot');
    } catch (err) {
      hideTyping();
      addMessage("I'm sorry, something went wrong. Please try again.", 'bot');
      console.error('AutoReplyAI chat error:', err);
    } finally {
      state.isLoading = false;
    }
  }

  // --- UI Helpers ---
  function addMessage(text, sender) {
    var container = document.getElementById('arai-messages');
    var msgEl = document.createElement('div');
    msgEl.className = 'arai-msg ' + (sender === 'user' ? 'arai-msg-user' : 'arai-msg-bot');

    if (sender === 'user') {
      msgEl.style.background = state.settings.primaryColor;
    }

    setText(msgEl, text);
    container.appendChild(msgEl);
    container.scrollTop = container.scrollHeight;

    state.messages.push({ text: text, sender: sender });
  }

  function showTyping() {
    var container = document.getElementById('arai-messages');
    var typing = document.createElement('div');
    typing.className = 'arai-typing';
    typing.id = 'arai-typing';
    for (var i = 0; i < 3; i++) {
      typing.appendChild(document.createElement('span'));
    }
    container.appendChild(typing);
    container.scrollTop = container.scrollHeight;
  }

  function hideTyping() {
    var el = document.getElementById('arai-typing');
    if (el) el.remove();
  }

  function applyColor(color) {
    var header = document.querySelector('#' + WIDGET_ID + ' .arai-header');
    var btn = document.getElementById('arai-toggle');
    var sendBtn = document.getElementById('arai-send');
    if (header) header.style.background = color;
    if (btn) btn.style.background = color;
    if (sendBtn) sendBtn.style.background = color;
  }

  // --- Init ---
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', buildWidget);
  } else {
    buildWidget();
  }
})();

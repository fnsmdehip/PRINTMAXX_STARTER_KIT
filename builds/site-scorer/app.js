// SiteScore - Website Performance Analyzer
// Uses Google PageSpeed Insights API (free, no key needed for basic usage)

(function () {
    'use strict';

    const PAGESPEED_API = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed';

    // DOM refs
    const scanForm = document.getElementById('scan-form');
    const urlInput = document.getElementById('url-input');
    const scanBtn = document.getElementById('scan-btn');
    const btnText = scanBtn.querySelector('.btn-text');
    const btnLoading = scanBtn.querySelector('.btn-loading');
    const resultsSection = document.getElementById('results');
    const errorSection = document.getElementById('error-section');
    const rescanBtn = document.getElementById('rescan-btn');
    const errorRetry = document.getElementById('error-retry');

    // Normalize URL
    function normalizeUrl(input) {
        let url = input.trim();
        if (!/^https?:\/\//i.test(url)) {
            url = 'https://' + url;
        }
        return url;
    }

    // Format URL for display
    function displayUrl(url) {
        return url.replace(/^https?:\/\//, '').replace(/\/$/, '');
    }

    // Set loading state
    function setLoading(loading) {
        scanBtn.disabled = loading;
        btnText.style.display = loading ? 'none' : '';
        btnLoading.style.display = loading ? 'inline' : 'none';
        urlInput.disabled = loading;
    }

    // Show error
    function showError(title, msg) {
        resultsSection.style.display = 'none';
        errorSection.style.display = 'block';
        document.getElementById('error-title').textContent = title;
        document.getElementById('error-msg').textContent = msg;
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Score color
    function getScoreColor(score) {
        if (score >= 90) return 'good';
        if (score >= 50) return 'ok';
        return 'bad';
    }

    function getScoreColorHex(score) {
        if (score >= 90) return '#22c55e';
        if (score >= 50) return '#eab308';
        return '#ef4444';
    }

    // Verdict text
    function getVerdict(score) {
        if (score >= 90) return 'Excellent. Your site is performing well.';
        if (score >= 75) return 'Good, but there is room to improve.';
        if (score >= 50) return 'Needs work. Several issues are hurting your site.';
        if (score >= 25) return 'Poor. Major issues detected across multiple areas.';
        return 'Critical. Your site has serious problems that need immediate attention.';
    }

    // Animate score ring
    function animateScore(score) {
        const ring = document.getElementById('score-ring-fill');
        const circumference = 2 * Math.PI * 54; // r=54
        const offset = circumference - (score / 100) * circumference;
        ring.style.strokeDasharray = circumference;
        ring.style.stroke = getScoreColorHex(score);

        // Trigger animation
        requestAnimationFrame(function () {
            ring.style.strokeDashoffset = offset;
        });

        // Animate number
        const scoreEl = document.getElementById('overall-score');
        let current = 0;
        const step = Math.max(1, Math.floor(score / 40));
        const interval = setInterval(function () {
            current += step;
            if (current >= score) {
                current = score;
                clearInterval(interval);
            }
            scoreEl.textContent = current;
        }, 30);
    }

    // Apply score class to card
    function applyScoreClass(cardId, score) {
        const card = document.getElementById(cardId);
        card.classList.remove('score-good', 'score-ok', 'score-bad');
        card.classList.add('score-' + getScoreColor(score));
    }

    // Create detail item
    function createDetailItem(name, desc, status) {
        var div = document.createElement('div');
        div.className = 'detail-item';
        div.innerHTML =
            '<div class="detail-status ' + status + '"></div>' +
            '<div class="detail-text">' +
            '<div class="detail-name">' + escapeHtml(name) + '</div>' +
            '<div class="detail-desc">' + escapeHtml(desc) + '</div>' +
            '</div>';
        return div;
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Extract audit results from PageSpeed API response
    function extractResults(data, url) {
        var lhr = data.lighthouseResult;
        var categories = lhr.categories || {};
        var audits = lhr.audits || {};

        // Performance score (0-100)
        var perfScore = categories.performance
            ? Math.round(categories.performance.score * 100)
            : 0;

        // SEO score
        var seoScore = categories.seo
            ? Math.round(categories.seo.score * 100)
            : 0;

        // Accessibility as a proxy for overall quality
        var a11yScore = categories.accessibility
            ? Math.round(categories.accessibility.score * 100)
            : 50;

        // Best practices
        var bpScore = categories['best-practices']
            ? Math.round(categories['best-practices'].score * 100)
            : 50;

        // Mobile friendliness
        var viewport = audits['viewport'] ? audits['viewport'].score === 1 : false;
        var fontSizeOk = audits['font-size'] ? audits['font-size'].score === 1 : true;
        var tapTargets = audits['tap-targets'] ? audits['tap-targets'].score === 1 : true;
        var mobileChecks = [viewport, fontSizeOk, tapTargets].filter(Boolean).length;
        var mobileScore = Math.round((mobileChecks / 3) * 100);

        // Adjust mobile score: if we got a mobile strategy response and performance is decent
        if (data.loadingExperience && data.loadingExperience.overall_category === 'FAST') {
            mobileScore = Math.max(mobileScore, 85);
        }

        // SSL check (URL starts with https)
        var isHttps = /^https:/i.test(url);
        var redirectsHttps = audits['redirects-http'] ? audits['redirects-http'].score === 1 : false;
        var sslScore = (isHttps || redirectsHttps) ? 100 : 0;

        // Security score
        var securityScore = sslScore;
        if (bpScore >= 80) securityScore = Math.max(securityScore, 80);

        // Load time metrics
        var fcp = audits['first-contentful-paint']
            ? audits['first-contentful-paint'].numericValue
            : null;
        var lcp = audits['largest-contentful-paint']
            ? audits['largest-contentful-paint'].numericValue
            : null;
        var si = audits['speed-index']
            ? audits['speed-index'].numericValue
            : null;
        var tti = audits['interactive']
            ? audits['interactive'].numericValue
            : null;
        var tbt = audits['total-blocking-time']
            ? audits['total-blocking-time'].numericValue
            : null;
        var cls = audits['cumulative-layout-shift']
            ? audits['cumulative-layout-shift'].numericValue
            : null;

        // SEO detail checks
        var hasTitle = audits['document-title'] ? audits['document-title'].score === 1 : false;
        var hasMeta = audits['meta-description'] ? audits['meta-description'].score === 1 : false;
        var hasH1 = audits['heading-order'] ? audits['heading-order'].score === 1 : true;
        var hasCanonical = audits['canonical'] ? audits['canonical'].score === 1 : false;
        var hasHreflang = audits['hreflang'] ? audits['hreflang'].score === 1 : true;
        var hasRobots = audits['robots-txt'] ? audits['robots-txt'].score === 1 : true;
        var isCrawlable = audits['is-crawlable'] ? audits['is-crawlable'].score === 1 : true;
        var hasStructuredData = audits['structured-data-json-ld'] ? true : false;
        var imageAlts = audits['image-alt'] ? audits['image-alt'].score === 1 : true;
        var linkText = audits['link-text'] ? audits['link-text'].score === 1 : true;

        // Image optimization
        var imagesOptimized = audits['uses-optimized-images']
            ? audits['uses-optimized-images'].score === 1
            : true;
        var nextGenImages = audits['uses-webp-images']
            ? audits['uses-webp-images'].score === 1
            : true;
        var responsiveImages = audits['uses-responsive-images']
            ? audits['uses-responsive-images'].score === 1
            : true;

        // Render blocking
        var renderBlocking = audits['render-blocking-resources']
            ? audits['render-blocking-resources'].score === 1
            : true;

        // HTTP/2
        var http2 = audits['uses-http2'] ? audits['uses-http2'].score === 1 : true;

        // Text compression
        var textCompression = audits['uses-text-compression']
            ? audits['uses-text-compression'].score === 1
            : true;

        // Overall score: weighted average
        var overall = Math.round(
            perfScore * 0.35 +
            seoScore * 0.25 +
            mobileScore * 0.15 +
            securityScore * 0.10 +
            bpScore * 0.15
        );

        return {
            overall: overall,
            performance: {
                score: perfScore,
                fcp: fcp,
                lcp: lcp,
                si: si,
                tti: tti,
                tbt: tbt,
                cls: cls
            },
            seo: {
                score: seoScore,
                hasTitle: hasTitle,
                hasMeta: hasMeta,
                hasH1: hasH1,
                hasCanonical: hasCanonical,
                isCrawlable: isCrawlable,
                imageAlts: imageAlts,
                linkText: linkText
            },
            mobile: {
                score: mobileScore,
                viewport: viewport,
                fontSizeOk: fontSizeOk,
                tapTargets: tapTargets
            },
            security: {
                score: securityScore,
                ssl: isHttps || redirectsHttps,
                http2: http2,
                bestPractices: bpScore
            },
            details: {
                imagesOptimized: imagesOptimized,
                nextGenImages: nextGenImages,
                responsiveImages: responsiveImages,
                renderBlocking: renderBlocking,
                textCompression: textCompression
            }
        };
    }

    // Format milliseconds
    function formatMs(ms) {
        if (ms == null) return '--';
        if (ms < 1000) return Math.round(ms) + 'ms';
        return (ms / 1000).toFixed(1) + 's';
    }

    // Render results
    function renderResults(results, url) {
        // Reset score ring
        var ring = document.getElementById('score-ring-fill');
        ring.style.strokeDashoffset = 339.292;

        // Overall
        animateScore(results.overall);
        document.getElementById('score-verdict').textContent = getVerdict(results.overall);

        // URL display
        document.getElementById('result-url').textContent = displayUrl(url);
        document.getElementById('scan-time').textContent = new Date().toLocaleString();

        // Performance card
        document.getElementById('perf-score').textContent = results.performance.score;
        document.getElementById('perf-detail').textContent =
            'LCP ' + formatMs(results.performance.lcp) +
            ' / FCP ' + formatMs(results.performance.fcp);
        applyScoreClass('perf-card', results.performance.score);

        // SEO card
        document.getElementById('seo-score').textContent = results.seo.score;
        var seoIssues = [
            !results.seo.hasTitle ? 'Missing title' : '',
            !results.seo.hasMeta ? 'No meta description' : '',
            !results.seo.isCrawlable ? 'Not crawlable' : ''
        ].filter(Boolean);
        document.getElementById('seo-detail').textContent =
            seoIssues.length ? seoIssues.join(', ') : 'Looking good';
        applyScoreClass('seo-card', results.seo.score);

        // Mobile card
        document.getElementById('mobile-score').textContent = results.mobile.score;
        document.getElementById('mobile-detail').textContent =
            results.mobile.viewport ? 'Viewport configured' : 'Missing viewport meta';
        applyScoreClass('mobile-card', results.mobile.score);

        // Security card
        document.getElementById('security-score').textContent = results.security.score;
        document.getElementById('security-detail').textContent =
            results.security.ssl ? 'SSL active' : 'No SSL detected';
        applyScoreClass('security-card', results.security.score);

        // Detail grid
        var grid = document.getElementById('detail-grid');
        grid.innerHTML = '';

        var detailItems = [
            {
                name: 'SSL / HTTPS',
                desc: results.security.ssl ? 'Connection is encrypted' : 'Site not using HTTPS. Major trust issue.',
                status: results.security.ssl ? 'pass' : 'fail'
            },
            {
                name: 'Page title',
                desc: results.seo.hasTitle ? 'Title tag present' : 'Missing title tag. Hurts search rankings.',
                status: results.seo.hasTitle ? 'pass' : 'fail'
            },
            {
                name: 'Meta description',
                desc: results.seo.hasMeta ? 'Meta description present' : 'Missing meta description. Lower click-through from Google.',
                status: results.seo.hasMeta ? 'pass' : 'fail'
            },
            {
                name: 'Mobile viewport',
                desc: results.mobile.viewport ? 'Viewport meta tag configured' : 'Missing viewport meta. Bad mobile experience.',
                status: results.mobile.viewport ? 'pass' : 'fail'
            },
            {
                name: 'First Contentful Paint',
                desc: formatMs(results.performance.fcp) + (results.performance.fcp && results.performance.fcp < 1800 ? ' (good)' : results.performance.fcp ? ' (slow)' : ''),
                status: results.performance.fcp && results.performance.fcp < 1800 ? 'pass' : results.performance.fcp && results.performance.fcp < 3000 ? 'warn' : 'fail'
            },
            {
                name: 'Largest Contentful Paint',
                desc: formatMs(results.performance.lcp) + (results.performance.lcp && results.performance.lcp < 2500 ? ' (good)' : results.performance.lcp ? ' (slow)' : ''),
                status: results.performance.lcp && results.performance.lcp < 2500 ? 'pass' : results.performance.lcp && results.performance.lcp < 4000 ? 'warn' : 'fail'
            },
            {
                name: 'Total Blocking Time',
                desc: formatMs(results.performance.tbt) + (results.performance.tbt != null && results.performance.tbt < 200 ? ' (good)' : results.performance.tbt != null ? ' (high)' : ''),
                status: results.performance.tbt != null && results.performance.tbt < 200 ? 'pass' : results.performance.tbt != null && results.performance.tbt < 600 ? 'warn' : 'fail'
            },
            {
                name: 'Cumulative Layout Shift',
                desc: results.performance.cls != null ? results.performance.cls.toFixed(3) + (results.performance.cls < 0.1 ? ' (good)' : ' (high, page shifts around)') : '--',
                status: results.performance.cls != null && results.performance.cls < 0.1 ? 'pass' : results.performance.cls != null && results.performance.cls < 0.25 ? 'warn' : 'fail'
            },
            {
                name: 'Font sizing',
                desc: results.mobile.fontSizeOk ? 'Text is legible on mobile' : 'Text too small on mobile devices',
                status: results.mobile.fontSizeOk ? 'pass' : 'warn'
            },
            {
                name: 'Tap targets',
                desc: results.mobile.tapTargets ? 'Buttons and links are properly sized' : 'Tap targets too small or too close together',
                status: results.mobile.tapTargets ? 'pass' : 'warn'
            },
            {
                name: 'Image optimization',
                desc: results.details.imagesOptimized ? 'Images are optimized' : 'Unoptimized images detected. Slowing page load.',
                status: results.details.imagesOptimized ? 'pass' : 'warn'
            },
            {
                name: 'Next-gen image formats',
                desc: results.details.nextGenImages ? 'Using WebP/AVIF' : 'Not using WebP or AVIF. Could reduce image size 25-50%.',
                status: results.details.nextGenImages ? 'pass' : 'warn'
            },
            {
                name: 'Render-blocking resources',
                desc: results.details.renderBlocking ? 'No render-blocking resources' : 'Render-blocking CSS/JS detected. Slows first paint.',
                status: results.details.renderBlocking ? 'pass' : 'warn'
            },
            {
                name: 'Text compression',
                desc: results.details.textCompression ? 'Gzip/Brotli enabled' : 'Text compression not enabled. Easy win for speed.',
                status: results.details.textCompression ? 'pass' : 'warn'
            },
            {
                name: 'Image alt attributes',
                desc: results.seo.imageAlts ? 'All images have alt text' : 'Some images missing alt text. Hurts SEO and accessibility.',
                status: results.seo.imageAlts ? 'pass' : 'warn'
            },
            {
                name: 'Crawlable',
                desc: results.seo.isCrawlable ? 'Search engines can crawl this page' : 'Page may be blocked from search engines.',
                status: results.seo.isCrawlable ? 'pass' : 'fail'
            }
        ];

        detailItems.forEach(function (item) {
            grid.appendChild(createDetailItem(item.name, item.desc, item.status));
        });

        // CTA
        document.getElementById('cta-score').textContent = results.overall;
        document.getElementById('cta-url-field').value = url;
        document.getElementById('cta-score-field').value = results.overall;

        // Show results
        errorSection.style.display = 'none';
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Main scan function
    async function scanSite(url) {
        setLoading(true);
        errorSection.style.display = 'none';
        resultsSection.style.display = 'none';

        try {
            // Run both mobile and desktop scans, use mobile as primary
            var apiUrl = PAGESPEED_API +
                '?url=' + encodeURIComponent(url) +
                '&strategy=mobile' +
                '&category=performance' +
                '&category=seo' +
                '&category=accessibility' +
                '&category=best-practices';

            var response = await fetch(apiUrl);

            if (!response.ok) {
                var errData = {};
                try { errData = await response.json(); } catch (e) { /* ignore */ }
                var errMsg = 'Could not analyze this URL.';
                if (errData.error && errData.error.message) {
                    errMsg = errData.error.message;
                }
                if (response.status === 400) {
                    errMsg = 'Invalid URL or the site could not be reached. Make sure the URL is correct and the site is publicly accessible.';
                }
                if (response.status === 429) {
                    errMsg = 'Rate limit reached. Wait a minute and try again.';
                }
                throw new Error(errMsg);
            }

            var data = await response.json();

            if (!data.lighthouseResult) {
                throw new Error('No analysis data returned. The site may be unreachable or blocking automated scans.');
            }

            var results = extractResults(data, url);
            renderResults(results, url);

        } catch (err) {
            var errorTitle = 'Scan failed';
            var errorMsg = err.message || 'Something went wrong. Try again.';

            if (err.message && err.message.includes('fetch')) {
                errorTitle = 'Network error';
                errorMsg = 'Could not reach the PageSpeed API. Check your internet connection and try again.';
            }

            showError(errorTitle, errorMsg);
        } finally {
            setLoading(false);
        }
    }

    // Event listeners
    scanForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var url = normalizeUrl(urlInput.value);
        urlInput.value = url;
        scanSite(url);
    });

    rescanBtn.addEventListener('click', function () {
        resultsSection.style.display = 'none';
        urlInput.value = '';
        urlInput.focus();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    errorRetry.addEventListener('click', function () {
        errorSection.style.display = 'none';
        urlInput.focus();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Handle CTA form submission with fallback
    var ctaForm = document.getElementById('cta-email-form');
    ctaForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var formData = new FormData(ctaForm);
        var email = formData.get('email');
        var scannedUrl = formData.get('scanned_url');
        var score = formData.get('score');

        // Try Formspree, fall back to mailto
        fetch(ctaForm.action, {
            method: 'POST',
            body: formData,
            headers: { 'Accept': 'application/json' }
        }).then(function (response) {
            if (response.ok) {
                ctaForm.innerHTML =
                    '<div style="padding:20px;color:#22c55e;font-weight:600;">' +
                    'Got it. We\'ll send your first report within 24 hours.' +
                    '</div>';
            } else {
                // Fallback: open mailto
                window.location.href = 'mailto:hello@sitescore.app?subject=SiteScore%20Monitoring&body=' +
                    encodeURIComponent('Email: ' + email + '\nURL: ' + scannedUrl + '\nScore: ' + score + '\n\nI want to start monitoring.');
                ctaForm.innerHTML =
                    '<div style="padding:20px;color:#eab308;font-weight:600;">' +
                    'Opening your email client. Send us the pre-filled email to get started.' +
                    '</div>';
            }
        }).catch(function () {
            window.location.href = 'mailto:hello@sitescore.app?subject=SiteScore%20Monitoring&body=' +
                encodeURIComponent('Email: ' + email + '\nURL: ' + scannedUrl + '\nScore: ' + score + '\n\nI want to start monitoring.');
            ctaForm.innerHTML =
                '<div style="padding:20px;color:#eab308;font-weight:600;">' +
                'Opening your email client. Send us the pre-filled email to get started.' +
                '</div>';
        });
    });

    // URL params: auto-scan if ?url= provided
    var params = new URLSearchParams(window.location.search);
    var autoUrl = params.get('url');
    if (autoUrl) {
        urlInput.value = normalizeUrl(autoUrl);
        scanSite(normalizeUrl(autoUrl));
    }
})();

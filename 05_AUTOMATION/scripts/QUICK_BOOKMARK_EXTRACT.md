# Quick Twitter Bookmark Extraction (2 Minutes)

## Step 1: Open Twitter Bookmarks
Navigate to: https://x.com/i/bookmarks

## Step 2: Open Console
Press: `Cmd + Option + I` (opens DevTools)
Click: "Console" tab

## Step 3: Paste This Script

```javascript
// Quick bookmark extractor
(async function() {
    console.log('🚀 Starting bookmark extraction...');

    const bookmarks = [];
    const seenUrls = new Set();
    let scrollAttempts = 0;
    const maxScrolls = 20;

    // Business keywords filter
    const businessKeywords = [
        'revenue', 'mrr', 'arr', 'users', 'growth', 'launch', 'build',
        'app', 'saas', 'startup', 'indie', 'maker', 'founder',
        'email', 'seo', 'marketing', 'conversion', 'funnel',
        'automation', 'ai', 'tool', 'product', 'api', 'code',
        'monetization', 'traffic', 'sales', '$', 'profit'
    ];

    function isBusinessContent(text) {
        if (!text || text.length < 50) return false;
        const lower = text.toLowerCase();
        return businessKeywords.some(kw => lower.includes(kw));
    }

    function extractHandle(url) {
        const match = url.match(/\/([^/]+)\/status\//);
        return match ? match[1] : 'unknown';
    }

    // Scroll and extract
    while (scrollAttempts < maxScrolls) {
        const tweets = document.querySelectorAll('article[data-testid="tweet"]');

        tweets.forEach(tweet => {
            try {
                const link = tweet.querySelector('a[href*="/status/"]');
                if (!link) return;

                let url = link.getAttribute('href');
                if (url.startsWith('/')) url = 'https://x.com' + url;

                if (seenUrls.has(url)) return;
                seenUrls.add(url);

                const textElem = tweet.querySelector('[data-testid="tweetText"]');
                const text = textElem ? textElem.innerText : '';

                if (isBusinessContent(text)) {
                    bookmarks.push({
                        url: url,
                        text: text,
                        handle: extractHandle(url)
                    });
                }
            } catch (e) {
                // Skip failed extractions
            }
        });

        window.scrollBy(0, 1000);
        await new Promise(resolve => setTimeout(resolve, 2000));
        scrollAttempts++;

        console.log(`📜 Scrolled ${scrollAttempts}/${maxScrolls}, found ${bookmarks.length} business bookmarks`);
    }

    console.log(`✅ Extraction complete! Found ${bookmarks.length} bookmarks`);
    console.log('📋 Copy this data:');
    console.log(JSON.stringify(bookmarks, null, 2));

    // Also download as file
    const dataStr = JSON.stringify(bookmarks, null, 2);
    const blob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `bookmarks_${Date.now()}.json`;
    a.click();

    console.log('💾 Also saved to Downloads folder');

    return bookmarks;
})();
```

## Step 4: Wait for Completion
- You'll see progress updates in console
- When done, a JSON file downloads automatically
- Also see all data in console (can copy)

## Step 5: Send Me the File
Upload the downloaded JSON file or paste the console output.

I'll process it and add to ALPHA_STAGING.csv.

---

**This takes 2 minutes and works with your already-logged-in Chrome.**

No closing browser needed. No new instances.

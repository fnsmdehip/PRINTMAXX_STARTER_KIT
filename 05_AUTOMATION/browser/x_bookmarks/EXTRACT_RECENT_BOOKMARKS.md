# Extract Last 6 Months of Bookmarks (Up-to-Date Strategies)

## The Problem
X/Twitter lazy-loads bookmarks. The script only sees what's currently rendered in the DOM (~35 tweets).

## Solution: Aggressive Scrolling + Time Filter

### Step 1: Run This Improved Script

1. Go to: https://x.com/i/bookmarks
2. Open DevTools: `Cmd + Option + I`
3. Console tab
4. Paste this **aggressive scroller**:

```javascript
// X Bookmarks - Last 6 Months Extractor
(async () => {
    console.log('🚀 Starting 6-month extraction with aggressive scrolling...');

    const SIX_MONTHS_AGO = new Date();
    SIX_MONTHS_AGO.setMonth(SIX_MONTHS_AGO.getMonth() - 6);
    console.log(`📅 Extracting bookmarks from ${SIX_MONTHS_AGO.toDateString()} onwards...`);

    const bookmarks = [];
    let scrollCount = 0;
    let staleScrolls = 0;
    let prevCount = 0;
    let oldestDate = new Date();
    let reachedCutoff = false;

    while (scrollCount < 500 && !reachedCutoff) { // Max 500 scrolls
        // Click all "Read more" buttons
        const readMoreButtons = document.querySelectorAll('[data-testid="tweet"] [role="button"]');
        for (const btn of readMoreButtons) {
            if (btn.innerText.includes('Show') || btn.innerText.includes('more')) {
                try { btn.click(); await new Promise(r => setTimeout(r, 50)); } catch (e) {}
            }
        }

        // Extract all visible tweets
        const tweets = document.querySelectorAll('[data-testid="tweet"]');

        for (const tweet of tweets) {
            try {
                const textElem = tweet.querySelector('[data-testid="tweetText"]');
                const text = textElem?.innerText || '';

                const authorElem = tweet.querySelector('[data-testid="User-Name"]');
                const authorText = authorElem?.innerText || '';
                const lines = authorText.split('\n');
                const author = lines[0] || '';
                const handle = lines.find(l => l.startsWith('@')) || '';

                const timeElem = tweet.querySelector('time');
                const timestamp = timeElem?.getAttribute('datetime') || '';
                const displayTime = timeElem?.innerText || '';

                const linkElem = tweet.querySelector('a[href*="/status/"]');
                let url = linkElem?.getAttribute('href') || '';
                if (url && !url.startsWith('http')) url = `https://x.com${url}`;

                const cardLink = tweet.querySelector('[data-testid="card.wrapper"] a');
                const externalUrl = cardLink?.getAttribute('href') || '';

                const images = tweet.querySelectorAll('[data-testid="tweetPhoto"] img');
                const imageUrls = Array.from(images).map(img => img.src).filter(src => !src.includes('profile'));

                const hasVideo = !!tweet.querySelector('video');

                if (text && url && timestamp) {
                    const tweetDate = new Date(timestamp);

                    // Track oldest date we've seen
                    if (tweetDate < oldestDate) {
                        oldestDate = tweetDate;
                    }

                    // Check if we've gone past 6 months
                    if (tweetDate < SIX_MONTHS_AGO) {
                        reachedCutoff = true;
                        console.log(`⏹️  Reached 6-month cutoff at ${tweetDate.toDateString()}`);
                    }

                    // Only add if within 6 months
                    if (tweetDate >= SIX_MONTHS_AGO) {
                        bookmarks.push({
                            text: text,
                            author: author,
                            handle: handle,
                            timestamp: timestamp,
                            display_time: displayTime,
                            url: url,
                            external_link: externalUrl,
                            has_images: imageUrls.length > 0,
                            image_count: imageUrls.length,
                            has_video: hasVideo,
                            word_count: text.split(/\s+/).length,
                            date: tweetDate.toISOString().split('T')[0]
                        });
                    }
                }
            } catch (e) {
                console.error('Error processing tweet:', e);
            }
        }

        // Dedupe
        const unique = {};
        bookmarks.forEach(b => unique[b.url] = b);
        const current = Object.keys(unique).length;

        console.log(`📊 Scroll ${scrollCount}: ${current} bookmarks | Oldest: ${oldestDate.toDateString()}`);

        // Check if we're stuck (no new bookmarks after 5 scrolls)
        if (current === prevCount) {
            staleScrolls++;
            if (staleScrolls >= 5 && !reachedCutoff) {
                console.log('⚠️  No new bookmarks after 5 scrolls. Might be at the end.');
                break;
            }
        } else {
            staleScrolls = 0; // Reset counter if we found new ones
        }

        prevCount = current;

        // AGGRESSIVE SCROLL - scroll more pixels to load faster
        window.scrollBy(0, window.innerHeight * 2);
        await new Promise(r => setTimeout(r, 800)); // Faster scrolling
        scrollCount++;

        // Every 50 scrolls, pause a bit to let X catch up
        if (scrollCount % 50 === 0) {
            console.log('⏸️  Brief pause to let X load...');
            await new Promise(r => setTimeout(r, 2000));
        }
    }

    // Final dedupe
    const final = Object.values(bookmarks.reduce((acc, b) => {
        acc[b.url] = b;
        return acc;
    }, {}));

    // Sort by date (newest first)
    final.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    // Download JSON
    const blob = new Blob([JSON.stringify(final, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `x_bookmarks_6months_${new Date().toISOString().split('T')[0]}.json`;
    a.click();

    console.log(`\n✅ EXTRACTION COMPLETE!`);
    console.log(`📊 Downloaded ${final.length} bookmarks from last 6 months`);
    console.log(`📅 Date range: ${final[final.length-1]?.date} to ${final[0]?.date}`);
    console.log(`📈 Stats:`);
    console.log(`   - With external links: ${final.filter(b => b.external_link).length}`);
    console.log(`   - With images: ${final.filter(b => b.has_images).length}`);
    console.log(`   - With videos: ${final.filter(b => b.has_video).length}`);
    console.log(`   - Long threads (100+ words): ${final.filter(b => b.word_count >= 100).length}`);
    console.log(`   - Average words: ${Math.round(final.reduce((s,b) => s + b.word_count, 0) / final.length)}`);

    return final;
})();
```

### Why This Works Better:

1. **6-Month Time Filter**: Automatically stops when it hits tweets older than 6 months
2. **Aggressive Scrolling**: Scrolls 2x viewport height instead of 1x (faster loading)
3. **Faster Intervals**: 800ms instead of 1500ms between scrolls
4. **Smart Stopping**: Stops if no new bookmarks after 5 scrolls OR when it hits 6-month mark
5. **Progress Tracking**: Shows oldest date found so you know how far back you've gone
6. **Periodic Pauses**: Every 50 scrolls, pauses for 2s to let X's lazy loading catch up

### Expected Results:

- Should get **hundreds** of bookmarks (not just 35)
- Only from last 6 months = most recent strategies
- Sorted by date (newest first)
- Full text extracted (after expanding "Read more")

### After Running:

1. Let it scroll for a few minutes (it'll go fast)
2. Watch console for "Reached 6-month cutoff" message
3. File downloads automatically
4. Move to: `/Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks/`
5. Tell me when done, I'll analyze it!

---

## Troubleshooting

**If it stops too early:**
- X might be rate-limiting the scroll
- Try increasing the pause from 800ms to 1200ms
- Or just run it again, it'll pick up where it left off

**If it's going too slow:**
- Reduce pause to 500ms (but might hit rate limits)
- Close other tabs to free up memory

**If you want MORE than 6 months:**
- Change `SIX_MONTHS_AGO.setMonth(SIX_MONTHS_AGO.getMonth() - 6);`
- To: `- 12` for 1 year, `- 3` for 3 months, etc.

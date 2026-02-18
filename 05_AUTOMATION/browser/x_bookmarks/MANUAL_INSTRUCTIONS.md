# X Bookmarks Extraction - Manual Method

Since automated browser connection is tricky, here's the fastest manual method:

## Option 1: Export Bookmarks with Browser DevTools (RECOMMENDED)

1. **Open X.com bookmarks in Brave** - Navigate to https://x.com/i/bookmarks
2. **Open DevTools** - Press `Cmd+Option+I` (Mac) or `F12`
3. **Open Console tab**
4. **Paste this script** and press Enter:

```javascript
// X Bookmarks Extractor
(async () => {
    console.log('🚀 Starting bookmark extraction...');

    const bookmarks = [];
    let scrollCount = 0;
    let prevCount = 0;

    while (scrollCount < 100) {
        // Get all tweets
        const tweets = document.querySelectorAll('[data-testid="tweet"]');

        for (const tweet of tweets) {
            try {
                const textElem = tweet.querySelector('[data-testid="tweetText"]');
                const text = textElem ? textElem.innerText : '';

                const authorElem = tweet.querySelector('[data-testid="User-Name"]');
                const author = authorElem ? authorElem.innerText.split('\\n')[0] : '';

                const timeElem = tweet.querySelector('time');
                const timestamp = timeElem ? timeElem.getAttribute('datetime') : '';

                const linkElem = tweet.querySelector('a[href*="/status/"]');
                let url = linkElem ? linkElem.getAttribute('href') : '';
                if (url && !url.startsWith('http')) {
                    url = `https://x.com${url}`;
                }

                if (text && url) {
                    bookmarks.push({ text, author, timestamp, url });
                }
            } catch (e) {
                // Skip errors
            }
        }

        // Remove duplicates
        const unique = {};
        bookmarks.forEach(b => unique[b.url] = b);
        const uniqueBookmarks = Object.values(unique);

        console.log(`📊 Collected ${uniqueBookmarks.length} bookmarks...`);

        if (uniqueBookmarks.length === prevCount) {
            console.log('✅ No new bookmarks. Done!');
            break;
        }

        prevCount = uniqueBookmarks.length;

        // Scroll
        window.scrollBy(0, window.innerHeight);
        await new Promise(r => setTimeout(r, 1500));
        scrollCount++;
    }

    // Download as JSON
    const dataStr = JSON.stringify(Object.values(bookmarks.reduce((acc, b) => {
        acc[b.url] = b;
        return acc;
    }, {})), null, 2);

    const blob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `x_bookmarks_${new Date().toISOString().split('T')[0]}.json`;
    a.click();

    console.log('✅ Download started!');
})();
```

5. **Wait** - The script will scroll and collect all bookmarks, then auto-download a JSON file
6. **Move the downloaded JSON** to `/Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks/`
7. **Run the analyzer** - See Option 2 below

---

## Option 2: Process Downloaded Bookmarks

Once you have the JSON file from Option 1, run:

```bash
cd /Users/macbookpro/Downloads/PRINTMAXX_STARTER_KIT/AUTOMATIONS/x_bookmarks
python3 analyze_bookmarks.py <your_downloaded_file.json>
```

This will filter and extract actionable insights.

---

## Option 3: Quick Chrome DevTools Scroll Method

1. Go to https://x.com/i/bookmarks
2. Open DevTools Console
3. Run this to auto-scroll:

```javascript
let scrolls = 0;
const interval = setInterval(() => {
    window.scrollBy(0, window.innerHeight);
    scrolls++;
    console.log(`Scrolled ${scrolls} times...`);
    if (scrolls >= 50) clearInterval(interval);
}, 1500);
```

4. Then run the extraction script from Option 1

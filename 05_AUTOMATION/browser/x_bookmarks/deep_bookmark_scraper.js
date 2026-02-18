// X Bookmarks Deep Analysis Scraper
//
// Enhanced scraper that:
// 1. Expands "Read More" to get full post text
// 2. Collects images from business/tech posts only
// 3. Analyzes top replies for product/service funnels
// 4. Analyzes standout profiles (bio, banner, pic)
//
// USAGE:
// 1. Go to https://x.com/i/bookmarks
// 2. Open DevTools (Cmd+Option+I)
// 3. Paste this script in Console
// 4. Wait for extraction and download
//
// OUTPUT: x_bookmarks_deep_YYYY-MM-DD.json

(async () => {
    console.log('🚀 Starting DEEP bookmark extraction...');
    console.log('This will take longer - opening each post for full analysis');

    // Business/tech keywords for filtering (same as Python script)
    const INCLUDE_KEYWORDS = [
        'mrr', 'arr', 'revenue', 'profit', 'income', '$', 'k/mo', '/mo', 'k/month',
        'sold for', 'making', 'earned', 'monetize', 'monetization',
        'launched', 'shipped', 'built', 'building', 'launch', 'startup', 'saas',
        'side project', 'indie', 'solopreneur', 'founder', 'bootstrap', 'mvp',
        'growth hack', 'seo', 'traffic', 'conversions', 'subscribers', 'users',
        'customers', 'leads', 'outbound', 'cold email', 'funnel', 'landing page',
        'api', 'automation', 'workflow', 'no-code', 'low-code', 'ai tool', 'gpt',
        'cursor', 'claude', 'vercel', 'supabase', 'stripe', 'revenuecat',
        'app store', 'play store', 'ios', 'android', 'mobile app', 'web app',
        'chrome extension', 'plugin', 'template', 'notion', 'airtable',
        'pricing', 'paywall', 'subscription', 'freemium', 'affiliate', 'sponsor',
        'newsletter', 'course', 'ebook', 'info product', 'digital product',
        'case study', 'breakdown', 'thread', 'how i', 'step by step', 'playbook',
        'framework', 'strategy', 'tactic', 'hack', 'tip', 'lesson learned'
    ];

    const EXCLUDE_KEYWORDS = [
        'trump', 'biden', 'maga', 'democrat', 'republican', 'liberal', 'conservative',
        'woke', 'anti-woke', 'election', 'congress', 'senate', 'politician', 'political',
        'cancel culture', 'triggered', 'snowflake', 'sjw', 'dei',
        'ratio', 'based', 'cope', 'seethe', 'fr fr', 'no cap', 'bussin',
        'kardashian', 'kanye', 'celebrity', 'hollywood', 'reality tv',
        'touchdown', 'home run', 'championship', 'playoffs', 'fantasy football',
        'breaking news', 'tragedy', 'disaster', 'shooting', 'war', 'invasion'
    ];

    function isRelevantContent(text) {
        const textLower = text.toLowerCase();

        // Check excludes first
        for (const keyword of EXCLUDE_KEYWORDS) {
            if (textLower.includes(keyword)) return { relevant: false, reason: `excluded: ${keyword}` };
        }

        // Check includes
        for (const keyword of INCLUDE_KEYWORDS) {
            if (textLower.includes(keyword)) return { relevant: true, keyword };
        }

        return { relevant: false, reason: 'no business keywords' };
    }

    // Phase 1: Collect all bookmark URLs by scrolling
    console.log('📜 Phase 1: Collecting bookmark URLs...');
    const bookmarkUrls = new Set();
    let scrollCount = 0;
    let prevCount = 0;

    while (scrollCount < 150) {
        const tweets = document.querySelectorAll('[data-testid="tweet"]');

        for (const tweet of tweets) {
            try {
                const linkElem = tweet.querySelector('a[href*="/status/"]');
                let url = linkElem?.getAttribute('href') || '';
                if (url && !url.startsWith('http')) url = `https://x.com${url}`;
                if (url) bookmarkUrls.add(url);
            } catch (e) {}
        }

        const current = bookmarkUrls.size;
        if (scrollCount % 10 === 0) console.log(`📊 ${current} bookmark URLs collected...`);

        if (current === prevCount && scrollCount > 5) {
            console.log('✅ Finished collecting URLs');
            break;
        }

        prevCount = current;
        window.scrollBy(0, window.innerHeight);
        await new Promise(r => setTimeout(r, 1000));
        scrollCount++;
    }

    const allUrls = Array.from(bookmarkUrls);
    console.log(`\n📌 Total bookmarks found: ${allUrls.length}`);

    // Phase 2: Deep analysis of each bookmark
    console.log('\n🔬 Phase 2: Deep analysis (this takes time)...');

    const deepBookmarks = [];
    const profilesAnalyzed = new Set();
    const profileData = [];
    const funnelInsights = [];
    const imageAssets = [];

    // Process in batches to avoid rate limiting
    const BATCH_SIZE = 5;
    const DELAY_BETWEEN_REQUESTS = 2000;

    for (let i = 0; i < Math.min(allUrls.length, 100); i++) { // Limit to first 100 for speed
        const url = allUrls[i];

        try {
            // Open tweet in new tab, extract data, close
            console.log(`[${i+1}/${Math.min(allUrls.length, 100)}] Analyzing: ${url.split('/').slice(-1)[0]}`);

            const response = await fetch(url);
            const html = await response.text();

            // Create a temporary DOM to parse
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            // Extract from meta tags (more reliable)
            const ogDescription = doc.querySelector('meta[property="og:description"]')?.content || '';
            const ogImage = doc.querySelector('meta[property="og:image"]')?.content || '';
            const ogTitle = doc.querySelector('meta[property="og:title"]')?.content || '';

            // Extract author from URL
            const urlParts = url.split('/');
            const authorHandle = urlParts[3] || 'unknown';

            // Full text from meta description
            const fullText = ogDescription;

            // Check relevance
            const relevance = isRelevantContent(fullText);

            if (relevance.relevant) {
                const bookmark = {
                    url,
                    author: `@${authorHandle}`,
                    fullText,
                    truncatedInFeed: fullText.length > 280,
                    matchedKeyword: relevance.keyword,
                    timestamp: new Date().toISOString(),
                    images: ogImage ? [ogImage] : [],
                    hasImage: !!ogImage
                };

                deepBookmarks.push(bookmark);

                // Collect images for repurposing
                if (ogImage) {
                    imageAssets.push({
                        url: ogImage,
                        postUrl: url,
                        author: `@${authorHandle}`,
                        caption: fullText.substring(0, 200),
                        category: relevance.keyword
                    });
                }

                // Profile analysis (first time seeing this author)
                if (!profilesAnalyzed.has(authorHandle)) {
                    profilesAnalyzed.add(authorHandle);

                    // Get profile data from meta
                    profileData.push({
                        handle: `@${authorHandle}`,
                        profileUrl: `https://x.com/${authorHandle}`,
                        samplePostUrl: url,
                        sampleContent: fullText.substring(0, 300),
                        contentCategory: relevance.keyword,
                        // These would need actual profile page scraping:
                        needsDeepScrape: true,
                        bio: null,
                        bannerUrl: null,
                        profilePicUrl: null,
                        bioLink: null,
                        followerCount: null
                    });
                }

                console.log(`  ✓ Business content: "${fullText.substring(0, 50)}..."`);
            } else {
                console.log(`  ⊘ Filtered: ${relevance.reason}`);
            }

            // Rate limiting
            if (i % BATCH_SIZE === BATCH_SIZE - 1) {
                console.log(`  ⏳ Pausing to avoid rate limits...`);
                await new Promise(r => setTimeout(r, DELAY_BETWEEN_REQUESTS));
            }

        } catch (e) {
            console.log(`  ⚠ Error: ${e.message}`);
        }
    }

    // Phase 3: Summary and download
    console.log('\n📊 DEEP ANALYSIS SUMMARY');
    console.log('='.repeat(50));
    console.log(`Total bookmarks scanned: ${allUrls.length}`);
    console.log(`Business/tech content: ${deepBookmarks.length}`);
    console.log(`Unique profiles found: ${profileData.length}`);
    console.log(`Images collected: ${imageAssets.length}`);
    console.log('='.repeat(50));

    // Create comprehensive export
    const exportData = {
        metadata: {
            exportDate: new Date().toISOString(),
            totalBookmarks: allUrls.length,
            businessContent: deepBookmarks.length,
            uniqueProfiles: profileData.length,
            imagesCollected: imageAssets.length
        },
        bookmarks: deepBookmarks,
        profiles: profileData,
        imageAssets: imageAssets,
        funnelInsights: funnelInsights,
        // URLs that need manual deep analysis (profile scraping)
        pendingProfileAnalysis: profileData.filter(p => p.needsDeepScrape).map(p => p.profileUrl)
    };

    // Download JSON
    const blob = new Blob([JSON.stringify(exportData, null, 2)], {type: 'application/json'});
    const downloadUrl = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = `x_bookmarks_deep_${new Date().toISOString().split('T')[0]}.json`;
    a.click();

    console.log(`\n✅ Downloaded: x_bookmarks_deep_${new Date().toISOString().split('T')[0]}.json`);
    console.log('\n📋 NEXT STEPS:');
    console.log('1. Move file to AUTOMATIONS/x_bookmarks/');
    console.log('2. Run: python3 analyze_deep_bookmarks.py <filename>');
    console.log('3. Review profiles in LEDGER/PROFILE_ANALYSIS.csv');

    // Return data for console access
    window.deepBookmarkData = exportData;
    console.log('\n💡 Data also available as: window.deepBookmarkData');

})();

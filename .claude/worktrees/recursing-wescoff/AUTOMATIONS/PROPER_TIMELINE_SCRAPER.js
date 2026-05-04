/**
 * PROPER TWITTER TIMELINE SCRAPER
 * Paste this in Chrome console while on x.com (logged in)
 * Scrapes actual tweets from timelines, expands "read more", gets full text
 */

(async function() {
    const accounts = [
        'levelsio', 'tdinh_me', 'codyschneiderxx', 'dannypostmaa', 'marc_louvion',
        'gregisenberg', 'pipelineabuser', 'knoxtwts', 'purpdevvv', 'iamgdsa',
        'jasoncfox', 'caiden_cole', 'maverickecom', 'Argona0x', 'WongKinYiu',
        'BFlowr', 'dansugcmodels', 'franci__ugc', 'Jonnyvandel', 'AntonioEscudero',
        'paoloanzn', 'yegormethod', 'simonecanciello', 'xivy0k', 'tatealax',
        'wesocialgrowth', 'ZignoiM', 'BLUECOW009', 'tom777kruise', 'eptwts',
        'zephyr_z9', 'gaborcselle', 'lilyraynyc', 'JohnMu', 'paborns',
        'AppTweak', 'seanb2b', '0xzak', 'Hightrafficsite', 'EliotPay',
        'anthilemoon', 'aaditsh', 'HarrisonCode', 'JumpyAnalysis', 'TheG0dlyOne',
        'lottsnomad', 'THArrowOfApollo', 'ShitpostGate', 'WilliamW_Stocks', 'TimSweeneyEpic',
        'DrPufferfish', 'demirdjiantwins', 'jacobrodri_', 'TheRealNatek', 'AlexHormozi',
        'The_Cass_Daily', 'MrBeast', 'LinusTech', 'MKBHD', 'naval',
        'balajis', 'elonmusk', 'sama', 'patrickc', 'benedictevans',
        'jwuphysics', 'karpathy', 'ylecun', 'goodfellow_ian', 'andrewchen',
        'rrhoover', 'Austen', 'ajlkn', 'zenorocha', 'wesbos',
        'addyosmani', 'sindresorhus', 'LeaVerou', 'sarah_edo', '_dte',
        'marcusmeurer', 'frankdilo', 'thisiskp_', 'arvidkahl', 'agazdecki',
        'tylertringas', 'patio11', 'swyx', 'Shpigford', 'csallen',
        'ecomceo'
    ];

    console.log('🚀 PROPER TIMELINE SCRAPER');
    console.log(`Scraping ${accounts.length} accounts`);
    console.log('This will take 45-60 minutes');
    console.log('='.repeat(60));

    const allTweets = [];
    let processedAccounts = 0;

    for (const handle of accounts) {
        processedAccounts++;
        console.log(`\n[${processedAccounts}/${accounts.length}] @${handle}`);

        // Navigate to profile
        window.location.href = `https://x.com/${handle}`;

        // Wait for page load
        await new Promise(r => setTimeout(r, 4000));

        // Scroll and extract tweets
        const tweets = [];
        for (let scroll = 0; scroll < 5; scroll++) {
            // Expand all "Show more" buttons
            document.querySelectorAll('[data-testid="tweet-text-show-more-link"]').forEach(btn => {
                try { btn.click(); } catch(e) {}
            });

            await new Promise(r => setTimeout(r, 500));

            // Extract tweets
            const articles = document.querySelectorAll('article[data-testid="tweet"]');

            articles.forEach(article => {
                try {
                    const link = article.querySelector('a[href*="/status/"]');
                    const textElem = article.querySelector('[data-testid="tweetText"]');

                    if (link && textElem) {
                        const url = link.href;
                        const text = textElem.innerText;

                        // Filter for actionable business content
                        const hasValue = (
                            text.length > 50 &&
                            (
                                // Tools mentioned
                                /\.(com|io|ai|app|co)\b/.test(text) ||
                                // Numbers/metrics
                                /\$\d+|revenue|mrr|arr|\d+%|\d+x/.test(text.toLowerCase()) ||
                                // Processes
                                /step\s+\d+|how\s+to|framework|playbook|guide/.test(text.toLowerCase()) ||
                                // Specific tactics
                                /filter\s+by|database|pull\s+every|install|tech\s+stack/.test(text.toLowerCase())
                            )
                        );

                        if (hasValue && !tweets.find(t => t.url === url)) {
                            tweets.push({
                                handle,
                                url,
                                text,
                                scraped_at: new Date().toISOString()
                            });
                        }
                    }
                } catch(e) {}
            });

            // Scroll down
            window.scrollBy(0, 800);
            await new Promise(r => setTimeout(r, 1500));
        }

        console.log(`  ✓ Found ${tweets.length} actionable tweets`);
        allTweets.push(...tweets);

        // Brief pause between accounts
        await new Promise(r => setTimeout(r, 2000));
    }

    // Download results
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    const filename = `twitter_timeline_scrape_${timestamp}.json`;

    const blob = new Blob([JSON.stringify(allTweets, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    console.log('\n✅ SCRAPING COMPLETE');
    console.log(`📊 Total tweets: ${allTweets.length}`);
    console.log(`📁 Downloaded: ${filename}`);
    console.log('\nNext: python3 AUTOMATIONS/process_console_scrape.py ~/Downloads/' + filename);

})();

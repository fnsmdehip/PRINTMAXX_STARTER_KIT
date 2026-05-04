/**
 * BULK HIGH-SIGNAL ACCOUNT SCRAPER
 * Run this ONCE in Chrome DevTools console while logged into X/Twitter
 *
 * HOW TO USE:
 * 1. Open x.com in your logged-in Chrome
 * 2. Open DevTools (Cmd+Option+I)
 * 3. Go to Console tab
 * 4. Paste this ENTIRE script
 * 5. Press Enter
 * 6. Wait 30-60 minutes (it will scrape all 92 accounts)
 * 7. Results will auto-download as JSON file
 */

(async function() {
    console.log('🚀 Starting bulk account scraper...');

    // List of 92 high-signal accounts (from HIGH_SIGNAL_SOURCES.csv)
    const accounts = [
        'levelsio', 'tdinh_me', 'pipelineabuser', 'knoxtwts', 'dannypostmaa',
        'marc_louvion', 'gregisenberg', 'codyschneiderxx', 'simonecanciello',
        'xivy0k', 'tatealax', 'wesocialgrowth', 'dansugcmodels', 'franci__ugc',
        'Jonnyvandel', 'AntonioEscudero', 'paoloanzn', 'yegormethod',
        'jasoncfox', 'iamgdsa', 'purpdevvv', 'saradietschy', 'iamAdamLovelace',
        'mattgrayyes', 'MrBeast', 'MKBHD', 'GaryVee', 'naval', 'elonmusk',
        'paulg', 'sama', 'dhh', 'jason', 'andrewchen', 'rrhoover', 'lennysan',
        'shreyas', 'jwmares', 'noah_edelman', 'petergyang', 'heyblake',
        'alexisohanian', 'hnshah', 'justinkan', 'darrenwaldron', 'ajlkn',
        'chrismessina', 'garyvee', 'neilpatel', 'randfish', 'timsoulo',
        'patrickc', 'polak_jasper', 'dagorenouf', 'callmemaybe', 'kylemcd',
        'tonydinh_', 'dannypostma', 'marclou', 'jonloomer', 'mattdistefano',
        'joisas', 'Marketingmax', 'rebekahradice', 'larrykim', 'sugarrae',
        'nealogrady', 'andreaconaill', 'Marketingmax', 'JuliaEMcCoy',
        'adamriemer', 'Mike_Stelzner', 'jaybaer', 'JoePulizzi', 'milesbeckler',
        'IanCleary', 'brianhonigman', 'AnnHandley', 'Marketingmax',
        'B3BCreations', 'BLUECOW009', 'maverickecom', 'Hightrafficsite',
        'zephyr_z9', 'eptwts', 'tom777kruise', 'TonyPepper', 'alexbrogan',
        'sweatystartup', 'robwalling', 'arvidkahl', 'businessbarista',
        'Nicolascole77', 'dickiebush', 'sahilbloom', 'MakadiaHarsh',
        'GrowthGuru_', 'ThisIsThomJames', 'morganhousel', 'jspujji'
    ];

    const businessKeywords = [
        'revenue', 'mrr', 'arr', 'users', 'growth', 'launch', 'build',
        'app', 'saas', 'startup', 'indie', 'maker', 'founder',
        'email', 'seo', 'marketing', 'conversion', 'funnel',
        'automation', 'ai', 'tool', 'product', 'api', 'code', '$'
    ];

    function isBusinessContent(text) {
        if (!text || text.length < 50) return false;
        const lower = text.toLowerCase();
        return businessKeywords.some(kw => lower.includes(kw));
    }

    async function scrapeAccount(handle) {
        console.log(`🔍 Scraping @${handle}...`);

        // Navigate to profile
        window.location.href = `https://x.com/${handle}`;

        // Wait for page load
        await new Promise(resolve => setTimeout(resolve, 3000));

        const tweets = [];
        const seen = new Set();

        // Scroll and collect tweets
        for (let scroll = 0; scroll < 5; scroll++) {
            const articles = document.querySelectorAll('article[data-testid="tweet"]');

            articles.forEach(article => {
                try {
                    const link = article.querySelector('a[href*="/status/"]');
                    if (!link) return;

                    const url = link.href;
                    if (seen.has(url)) return;
                    seen.add(url);

                    const textElem = article.querySelector('[data-testid="tweetText"]');
                    const text = textElem ? textElem.innerText : '';

                    if (isBusinessContent(text)) {
                        tweets.push({
                            url,
                            text,
                            handle,
                            scraped_at: new Date().toISOString()
                        });
                    }
                } catch (e) {
                    // Skip errors
                }
            });

            // Scroll down
            window.scrollBy(0, 800);
            await new Promise(resolve => setTimeout(resolve, 1500));
        }

        console.log(`  ✓ Found ${tweets.length} business tweets from @${handle}`);
        return tweets;
    }

    // Scrape all accounts sequentially
    const allTweets = [];
    let completed = 0;

    for (const account of accounts) {
        try {
            const tweets = await scrapeAccount(account);
            allTweets.push(...tweets);
            completed++;
            console.log(`📊 Progress: ${completed}/${accounts.length} accounts (${allTweets.length} total tweets)`);
        } catch (error) {
            console.error(`❌ Error scraping @${account}:`, error);
        }

        // Small delay between accounts
        await new Promise(resolve => setTimeout(resolve, 2000));
    }

    console.log(`\n✅ SCRAPING COMPLETE`);
    console.log(`📊 Total: ${allTweets.length} business tweets from ${completed} accounts`);

    // Download results as JSON
    const dataStr = JSON.stringify(allTweets, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `twitter_high_signal_${Date.now()}.json`;
    link.click();

    console.log('💾 Results downloaded. Save the file and run:');
    console.log('python3 AUTOMATIONS/process_console_scrape.py <filename>');

    return allTweets;
})();

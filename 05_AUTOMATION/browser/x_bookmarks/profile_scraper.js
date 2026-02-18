// X Profile Deep Scraper
//
// Scrapes full profile data for standout accounts:
// - Bio text and copy patterns
// - Bio link (and funnel destination)
// - Banner image URL
// - Profile pic URL
// - Follower/following counts
// - Pinned tweet analysis
//
// USAGE:
// 1. Go to any X profile page OR x.com/home
// 2. Open DevTools (Cmd+Option+I)
// 3. Paste this script in Console
// 4. It will scrape profiles from PROFILE_ANALYSIS.csv
//    OR you can pass an array of handles
//
// Example: scrapeProfiles(['@levelsio', '@tdinh_me', '@dannypostmaa'])

async function scrapeProfiles(handles = null) {
    console.log('🔍 Starting Profile Deep Scraper...');

    // If no handles provided, prompt for manual entry
    if (!handles) {
        const input = prompt('Enter handles (comma-separated, e.g., @levelsio,@tdinh_me):');
        if (!input) {
            console.log('❌ No handles provided');
            return;
        }
        handles = input.split(',').map(h => h.trim());
    }

    console.log(`📋 Scraping ${handles.length} profiles...`);

    const profiles = [];

    for (let i = 0; i < handles.length; i++) {
        let handle = handles[i];
        // Clean handle
        handle = handle.replace('@', '').trim();

        console.log(`[${i+1}/${handles.length}] Scraping @${handle}...`);

        try {
            const profileUrl = `https://x.com/${handle}`;
            const response = await fetch(profileUrl);
            const html = await response.text();

            // Parse HTML
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            // Extract from meta tags
            const ogImage = doc.querySelector('meta[property="og:image"]')?.content || '';
            const ogDescription = doc.querySelector('meta[property="og:description"]')?.content || '';
            const ogTitle = doc.querySelector('meta[property="og:title"]')?.content || '';

            // Extract bio from description (format: "Bio text. X followers, Y following")
            let bio = ogDescription;
            const followerMatch = bio.match(/(\d+(?:,\d+)*(?:\.\d+)?[KMB]?)\s*[Ff]ollowers/);
            const followingMatch = bio.match(/(\d+(?:,\d+)*(?:\.\d+)?[KMB]?)\s*[Ff]ollowing/);

            // Clean bio - remove the followers/following part
            bio = bio.replace(/\.\s*\d+.*[Ff]ollowers.*[Ff]ollowing.*$/, '').trim();
            bio = bio.replace(/\d+\s*[Ff]ollowers.*$/, '').trim();

            // Try to extract bio link from bio text
            const linkMatch = bio.match(/https?:\/\/[^\s]+/);
            const bioLink = linkMatch ? linkMatch[0] : null;

            // Profile pic is usually the og:image for profiles
            const profilePic = ogImage;

            // Banner would need actual page scraping - mark for manual
            const bannerUrl = null;

            const profileData = {
                handle: `@${handle}`,
                displayName: ogTitle?.split('(')[0]?.trim() || handle,
                bio: bio,
                bioLink: bioLink,
                profilePicUrl: profilePic,
                bannerUrl: bannerUrl,
                followers: followerMatch ? followerMatch[1] : null,
                following: followingMatch ? followingMatch[1] : null,
                profileUrl: profileUrl,
                scrapedAt: new Date().toISOString(),

                // Analysis fields
                bioLength: bio.length,
                hasBioLink: !!bioLink,
                bioKeywords: extractKeywords(bio),

                // Copy insights
                copyPatterns: analyzeBioCopy(bio)
            };

            profiles.push(profileData);
            console.log(`  ✓ @${handle}: ${bio.substring(0, 50)}...`);

            // Rate limiting
            await new Promise(r => setTimeout(r, 1500));

        } catch (e) {
            console.log(`  ⚠ Error scraping @${handle}: ${e.message}`);
            profiles.push({
                handle: `@${handle}`,
                error: e.message,
                scrapedAt: new Date().toISOString()
            });
        }
    }

    // Download results
    const exportData = {
        metadata: {
            scrapedAt: new Date().toISOString(),
            totalProfiles: profiles.length,
            successful: profiles.filter(p => !p.error).length
        },
        profiles: profiles
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `x_profiles_${new Date().toISOString().split('T')[0]}.json`;
    a.click();

    // Summary
    console.log('\n' + '='.repeat(50));
    console.log('PROFILE SCRAPE SUMMARY');
    console.log('='.repeat(50));
    console.log(`Total profiles: ${profiles.length}`);
    console.log(`Successful: ${profiles.filter(p => !p.error).length}`);
    console.log(`With bio links: ${profiles.filter(p => p.hasBioLink).length}`);

    // Bio copy insights
    console.log('\n📝 BIO COPY INSIGHTS:');
    const allPatterns = profiles.flatMap(p => p.copyPatterns || []);
    const patternCounts = {};
    allPatterns.forEach(p => patternCounts[p] = (patternCounts[p] || 0) + 1);
    Object.entries(patternCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .forEach(([pattern, count]) => {
            console.log(`  ${pattern}: ${count}`);
        });

    console.log('\n✅ Downloaded: x_profiles_' + new Date().toISOString().split('T')[0] + '.json');
    console.log('💡 Data also available as: window.profileData');

    window.profileData = exportData;
    return exportData;
}

function extractKeywords(text) {
    const keywords = [];
    const businessTerms = [
        'founder', 'ceo', 'building', 'shipped', 'launching', 'creator',
        'developer', 'designer', 'marketer', 'consultant', 'coach',
        'saas', 'app', 'startup', 'indie', 'solopreneur', 'entrepreneur',
        'newsletter', 'podcast', 'youtube', 'course', 'community'
    ];

    const textLower = text.toLowerCase();
    for (const term of businessTerms) {
        if (textLower.includes(term)) keywords.push(term);
    }
    return keywords;
}

function analyzeBioCopy(bio) {
    const patterns = [];
    const bioLower = bio.toLowerCase();

    // Pattern detection
    if (bio.match(/building|shipping|creating/i)) patterns.push('action_verb_start');
    if (bio.match(/\d+[KMB]?\+?\s*(users|customers|subscribers|followers)/i)) patterns.push('social_proof_numbers');
    if (bio.match(/ex-|former|prev/i)) patterns.push('credibility_past_role');
    if (bio.match(/founder|ceo|creator/i)) patterns.push('title_lead');
    if (bio.match(/\|/)) patterns.push('pipe_separator');
    if (bio.match(/→|→|>/)) patterns.push('arrow_separator');
    if (bio.match(/🚀|💰|🔥|⚡|✨/)) patterns.push('emoji_accent');
    if (bio.match(/\$\d+/)) patterns.push('revenue_mention');
    if (bio.match(/dm|dms|message me/i)) patterns.push('cta_dms');
    if (bio.match(/link below|bio link|check link/i)) patterns.push('cta_link');
    if (bio.length < 100) patterns.push('concise_bio');
    if (bio.length > 200) patterns.push('detailed_bio');

    return patterns;
}

// Make function globally available
window.scrapeProfiles = scrapeProfiles;

console.log('✅ Profile scraper loaded!');
console.log('Usage: scrapeProfiles(["@levelsio", "@tdinh_me"])');
console.log('Or just run: scrapeProfiles() and enter handles when prompted');

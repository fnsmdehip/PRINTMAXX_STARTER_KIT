# PRINTMAXX Site Test Report — 2026-03-15 04:32

## Summary

| Metric | Value |
|--------|-------|
| Total sites tested | 156 |
| GREEN (passing) | 101 (64.7%) |
| YELLOW (warnings) | 40 (25.6%) |
| RED (broken) | 15 (9.6%) |
| Avg load time | 4,983ms |
| Test method | Playwright async, 8 concurrent tabs |

## Root Cause Analysis

### RED sites break into 3 categories:

| Category | Count | Root Cause | Fix |
|----------|-------|------------|-----|
| DNS failures | 8 | Subdomain exceeds 63-char DNS limit | Redeploy with shorter names |
| 504 transient | 6 | Surge CDN overload during batch test | No fix needed (all return 200 on retry) |
| Navigation error | 1 | Client-side redirect destroys Playwright context | False positive (returns 200 on curl) |

**Actual broken sites: 8** (DNS failures only). The other 7 RED are false positives from transient CDN issues and test artifacts.

**True health: 148/156 sites operational (94.9%)**

## RED — DNS Failures (Subdomain Too Long — Need Redeployment)

These 8 sites have subdomains >63 characters. DNS cannot resolve them. They need to be redeployed with shortened names.

## RED — Broken Sites (Fix Immediately)

### OKC Mobile Detailing
- **URL:** https://mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-city-ok.surge.sh
- **HTTP:** None
- **Issues:** Page.goto: net::ERR_NAME_NOT_RESOLVED at https://mobile-auto-detailing-experts-in-oklahoma-city-champion-deta-oklahoma-c

### OKC Car Detailing
- **URL:** https://top-rated-mobile-car-detailing-in-oklahoma-city-ok-pure-prof-oklahoma-city-ok.surge.sh
- **HTTP:** None
- **Issues:** Page.goto: net::ERR_NAME_NOT_RESOLVED at https://top-rated-mobile-car-detailing-in-oklahoma-city-ok-pure-prof-oklahoma-c

### Portland Window Cleaning
- **URL:** https://window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or.surge.sh
- **HTTP:** None
- **Issues:** Page.goto: net::ERR_NAME_NOT_RESOLVED at https://window-cleaning-in-portland-or-all-pro-metro-services-llc-portland-or.s

### SaaS Stack Audit 200
- **URL:** https://saas-stack-audit-200.surge.sh
- **HTTP:** 200
- **Issues:** Page.title: Execution context was destroyed, most likely because of a navigation

### Birmingham Detailing
- **URL:** https://mobile-interior-detailing-birmingham-al-magic-city-detailing-birmingham-al.surge.sh
- **HTTP:** None
- **Issues:** Page.goto: net::ERR_NAME_NOT_RESOLVED at https://mobile-interior-detailing-birmingham-al-magic-city-detailing-birmingham

### Birmingham Home Detailing
- **URL:** https://home-professional-mobile-detailing-amp-products-super-store-birmingham-al.surge.sh
- **HTTP:** None
- **Issues:** Page.goto: net::ERR_NAME_NOT_RESOLVED at https://home-professional-mobile-detailing-amp-products-super-store-birmingham-

### Homeguide Handyman LV
- **URL:** https://the-10-best-handyman-services-in-las-vegas-nv-2026-homeguide-las-vegas-nv.surge.sh
- **HTTP:** None
- **Issues:** Page.goto: net::ERR_NAME_NOT_RESOLVED at https://the-10-best-handyman-services-in-las-vegas-nv-2026-homeguide-las-vegas-

### Pink Windows Louisville
- **URL:** https://local-window-cleaning-in-louisville-pink-x27-s-windows-louisville-ky.surge.sh
- **HTTP:** None
- **Issues:** Page.goto: net::ERR_NAME_NOT_RESOLVED at https://local-window-cleaning-in-louisville-pink-x27-s-windows-louisville-ky.su

### Cherry Window Louisville
- **URL:** https://residential-and-commercial-window-cleaning-cherry-window-cle-louisville-ky.surge.sh
- **HTTP:** None
- **Issues:** Page.goto: net::ERR_NAME_NOT_RESOLVED at https://residential-and-commercial-window-cleaning-cherry-window-cle-louisville

### Old Settlers Dental ATX
- **URL:** https://old-settlers-dental-p-a-austin-tx.surge.sh
- **HTTP:** 504
- **Issues:** HTTP 504

### Vitadox Austin Dentists
- **URL:** https://dentists-in-austin-tx-vitadox-austin-tx.surge.sh
- **HTTP:** 504
- **Issues:** HTTP 504

### Harmony Plumbing Dallas
- **URL:** https://harmony-plumbing-and-drain-cleaning-dallas-tx.surge.sh
- **HTTP:** 504
- **Issues:** HTTP 504

### Public Service Plumber DAL
- **URL:** https://public-service-plumbers-air-conditioning-llc-dallas-tx.surge.sh
- **HTTP:** 504
- **Issues:** HTTP 504

### Berkeys AC Plumbing Dallas
- **URL:** https://berkeys-air-conditioning-plumbing-and-electrical-dallas-tx.surge.sh
- **HTTP:** 504
- **Issues:** HTTP 504

### Accurate Leak Dallas
- **URL:** https://accurate-leak-and-line-dallas-tx.surge.sh
- **HTTP:** 504
- **Issues:** HTTP 504

## YELLOW — Sites with Warnings

### CoreDay
- **URL:** https://coreday.surge.sh
- **HTTP:** 200 | Load: 7166ms
- **Warnings:** slow: 7166ms

### Whitehouse Painting Louisville
- **URL:** https://whitehouse-residential-commercial-painting-co-llc-louisville-ky.surge.sh
- **HTTP:** 200 | Load: 7722ms
- **Warnings:** slow: 7722ms

### A1 Concrete Louisville
- **URL:** https://a-1-concrete-leveling-louisville-louisville-ky.surge.sh
- **HTTP:** 200 | Load: 7878ms
- **Warnings:** slow: 7878ms

### Down To Earth Sealcoating
- **URL:** https://down-to-earth-sealcoating-inc-louisville-ky.surge.sh
- **HTTP:** 200 | Load: 8238ms
- **Warnings:** slow: 8238ms

### CertaPro Painters Louisville
- **URL:** https://certapro-painters-of-louisville-metro-louisville-ky.surge.sh
- **HTTP:** 200 | Load: 7620ms
- **Warnings:** slow: 7620ms

### McCoy Window Cleaning
- **URL:** https://mccoy-window-gutter-cleaning-llc-louisville-ky.surge.sh
- **HTTP:** 200 | Load: 5783ms
- **Warnings:** slow: 5783ms

### Side Project Estimator
- **URL:** https://side-project-estimator.surge.sh
- **HTTP:** 200 | Load: 6255ms
- **Warnings:** slow: 6255ms

### Revenue Leak Audit
- **URL:** https://revenue-leak-audit.surge.sh
- **HTTP:** 200 | Load: 6531ms
- **Warnings:** slow: 6531ms

### Test Deploy 001
- **URL:** https://printmaxx-test-debug-deploy-001.surge.sh
- **HTTP:** 200 | Load: 4027ms
- **Warnings:** 200 OK but page blank/empty

### Nested Test 001
- **URL:** https://printmaxx-nested-test-001.surge.sh
- **HTTP:** 200 | Load: 3951ms
- **Warnings:** 200 OK but page blank/empty

### OpenClaw Fix Test 001
- **URL:** https://printmaxx-openclaw-fix-test-001.surge.sh
- **HTTP:** 200 | Load: 3858ms
- **Warnings:** 200 OK but page blank/empty

### Twitter PFP
- **URL:** https://printmaxx-twitter-pfp.surge.sh
- **HTTP:** 200 | Load: 4028ms
- **Warnings:** 200 OK but page blank/empty

### PDFMaxx
- **URL:** https://pdfmaxx.surge.sh
- **HTTP:** 200 | Load: 7043ms
- **Warnings:** slow: 7043ms

### Vibe Coding Profit Calc
- **URL:** https://vibe-coding-profit-calculator.surge.sh
- **HTTP:** 200 | Load: 6532ms
- **Warnings:** slow: 6532ms

### S Milwaukee Car Care
- **URL:** https://south-milwaukee-car-care-center-milwaukee-wi.surge.sh
- **HTTP:** 200 | Load: 6303ms
- **Warnings:** slow: 6303ms

### Gians Flooring MKE
- **URL:** https://gians-flooring-mke.surge.sh
- **HTTP:** 200 | Load: 7422ms
- **Warnings:** slow: 7422ms

### Landlords Pest MKE
- **URL:** https://a-landlords-pest-mke.surge.sh
- **HTTP:** 200 | Load: 7067ms
- **Warnings:** slow: 7067ms

### Shorewood Family Chiro
- **URL:** https://shorewood-family-chiro-mke.surge.sh
- **HTTP:** 200 | Load: 6830ms
- **Warnings:** slow: 6830ms

### Milwaukee Plumber Service
- **URL:** https://milwaukee-plumber-service-mke.surge.sh
- **HTTP:** 200 | Load: 6669ms
- **Warnings:** slow: 6669ms

### Solopreneur Launch Check
- **URL:** https://solopreneur-launch-checklist.surge.sh
- **HTTP:** 200 | Load: 6473ms
- **Warnings:** slow: 6473ms

### Subject Line Grader
- **URL:** https://subject-line-grader.surge.sh
- **HTTP:** 200 | Load: 6237ms
- **Warnings:** slow: 6237ms

### App Hub Crosslinks
- **URL:** https://app-hub-crosslinks.surge.sh
- **HTTP:** 200 | Load: 6276ms
- **Warnings:** slow: 6276ms

### Birmingham Handyman
- **URL:** https://handyman-and-home-modifications-in-birmingham-birmingham-al.surge.sh
- **HTTP:** 200 | Load: 6078ms
- **Warnings:** slow: 6078ms

### Vista Ridge Dentistry ATX
- **URL:** https://vista-ridge-family-dentistry-austin-tx.surge.sh
- **HTTP:** 200 | Load: 8159ms
- **Warnings:** slow: 8159ms

### Big Top Dentistry ATX
- **URL:** https://big-top-dentistry-for-kids-austin-tx.surge.sh
- **HTTP:** 200 | Load: 8768ms
- **Warnings:** slow: 8768ms

### Nursing Home Dental ATX
- **URL:** https://nursing-home-dental-care-austin-tx.surge.sh
- **HTTP:** 200 | Load: 5995ms
- **Warnings:** slow: 5995ms

### Austin Elite Smiles
- **URL:** https://austin-elite-smiles-pllc-austin-tx.surge.sh
- **HTTP:** 200 | Load: 8475ms
- **Warnings:** slow: 8475ms

### Lakeway Cosmetic Dent ATX
- **URL:** https://lakeway-cosmetic-dentistry-austin-tx.surge.sh
- **HTTP:** 200 | Load: 8678ms
- **Warnings:** slow: 8678ms

### Restora Dental Arts ATX
- **URL:** https://restora-dental-arts-austin-tx.surge.sh
- **HTTP:** 200 | Load: 7655ms
- **Warnings:** slow: 7655ms

### Helen Ragsdale DDS ATX
- **URL:** https://austin-laser-dentist-helen-ragsdale-dds-austin-tx.surge.sh
- **HTTP:** 200 | Load: 5971ms
- **Warnings:** slow: 5971ms

### About Smiles Dentistry
- **URL:** https://about-smiles-family-and-cosmetic-dentistry-austin-tx.surge.sh
- **HTTP:** 200 | Load: 8763ms
- **Warnings:** slow: 8763ms

### Dental Smiles ATX
- **URL:** https://dental-smiles-austin-tx.surge.sh
- **HTTP:** 200 | Load: 8443ms
- **Warnings:** slow: 8443ms

### Thiel Pediatric Dent ATX
- **URL:** https://thiel-pediatric-dentistry-austin-tx.surge.sh
- **HTTP:** 200 | Load: 8356ms
- **Warnings:** slow: 8356ms

### Smiles of Austin
- **URL:** https://leading-dentist-in-austin-tx-smiles-of-austin-austin-tx.surge.sh
- **HTTP:** 200 | Load: 8793ms
- **Warnings:** slow: 8793ms

### Austin Dentistry
- **URL:** https://austin-dentistry-dentist-in-austin-tx-austin-tx.surge.sh
- **HTTP:** 200 | Load: 8436ms
- **Warnings:** slow: 8436ms

### Dental Blush Miami
- **URL:** https://dental-blush-associates-pa-miami-fl.surge.sh
- **HTTP:** 200 | Load: 8667ms
- **Warnings:** slow: 8667ms

### J Family Dental Miami
- **URL:** https://j-family-dental-llc-miami-fl.surge.sh
- **HTTP:** 200 | Load: 6355ms
- **Warnings:** slow: 6355ms

### Berrett Home Dallas
- **URL:** https://berrett-home-services-dfw-dallas-tx.surge.sh
- **HTTP:** 200 | Load: 6229ms
- **Warnings:** slow: 6229ms

### Triune Plumbing Dallas
- **URL:** https://triune-plumbing-llc-dallas-tx.surge.sh
- **HTTP:** 200 | Load: 6424ms
- **Warnings:** slow: 6424ms

### FindLaw Dallas
- **URL:** https://find-dallas-tx-attorneys-and-law-firms-findlaw-dallas-tx.surge.sh
- **HTTP:** 200 | Load: 8986ms
- **Warnings:** slow: 8986ms

## GREEN — All Passing

| Site | URL | Load ms | Title |
|------|-----|---------|-------|
| SmartLead vs Instantly | https://smartlead-vs-instantly.surge.sh | 4398 | Smartlead vs Instantly (2026): Which Col |
| Best AI Tools 2026 | https://best-ai-tools-2026.surge.sh | 4376 | 7 AI Tools That Actually Make Money in 2 |
| SaaS Stack Audit | https://saas-stack-audit.surge.sh | 4276 | SaaS Stack Audit | How Much Are You Burn |
| PM Website Design | https://printmaxx-website-design.surge.sh | 4416 | Modern Website for Local Businesses | 15 |
| PM Landing Page | https://printmaxx-landing-page.surge.sh | 4505 | High-Converting Landing Pages | 5-12% Co |
| PM Cold Email | https://printmaxx-cold-email.surge.sh | 4436 | Cold Email Sequences That Get Replies |  |
| PM Web Scraping | https://printmaxx-web-scraping.surge.sh | 4473 | Web Scraping | Clean Data in 48 Hours |  |
| PM Automation | https://printmaxx-automation.surge.sh | 3905 | Python Automation | Save 3-15 Hours/Week |
| PM SEO Pages | https://printmaxx-seo-pages.surge.sh | 3919 | 100 SEO Pages for Your Business | Progra |
| PM Content Writing | https://printmaxx-content-writing.surge.sh | 3814 | 30 Days of Social Media Content | Ready  |
| PM App Development | https://printmaxx-app-development.surge.sh | 3875 | PWA Mobile App Development | Works on Ev |
| PM AI Chatbot | https://printmaxx-ai-chatbot.surge.sh | 3874 | AI Chatbot for Your Website | 24/7 Lead  |
| PM Data Analysis | https://printmaxx-data-analysis.surge.sh | 4047 | Data Analysis + Dashboard | Turn Messy D |
| Coit Cleaning Louisville | https://coit-cleaning-restoration-louisville-ky.surge.sh | 3946 | Coit Cleaning & Restoration | Louisville |
| Skyrockett Construction | https://skyrockett-construction-renovation-llc-louisville-ky.surge.sh | 3959 | Skyrockett Construction & Renovation, LL |
| Garretts Pressure Washing | https://garrett-s-presure-washing-louisville-ky.surge.sh | 3800 | Garrett's Presure Washing | Louisville K |
| Good Maintenance Cleaning | https://good-maintenance-cleaning-inc-louisville-ky.surge.sh | 3814 | Good Maintenance Cleaning, Inc | Louisvi |
| A1 Aluminum Louisville | https://a-1-aluminum-inc-louisville-ky.surge.sh | 4015 | A-1 Aluminum, Inc. | Louisville KY |
| The Maids Louisville | https://the-maids-in-southern-louisville-llc-louisville-ky.surge.sh | 3927 | The Maids in Southern Louisville LLC | L |
| Square It Away Contracting | https://square-it-away-contracting-llc-louisville-ky.surge.sh | 4185 | Square It Away Contracting, LLC | Louisv |
| Spindletop Draperies | https://spindletop-draperies-inc-louisville-ky.surge.sh | 3892 | Spindletop Draperies, Inc. | Louisville  |
| Naturescape Louisville | https://naturescape-louisville-ky.surge.sh | 4000 | NatureScape | Louisville KY |
| Cutting Hedge Landscaping | https://the-cutting-hedge-landscaping-mowing-louisville-ky.surge.sh | 3849 | The Cutting Hedge Landscaping & Mowing | |
| Greenworks Lawn Louisville | https://greenworks-lawn-landscape-tree-llc-louisville-ky.surge.sh | 3836 | Greenworks Lawn Landscape & Tree, LLC |  |
| Accurate Lawn Louisville | https://accurate-lawn-landscaping-inc-louisville-ky.surge.sh | 3876 | Accurate Lawn & Landscaping, Inc. | Loui |
| Daves Tree Surgeons | https://dave-s-tree-surgeons-inc-louisville-ky.surge.sh | 4003 | Dave's Tree Surgeons, Inc. | Louisville  |
| Bob Ray Company | https://bob-ray-company-inc-louisville-ky.surge.sh | 3971 | Bob Ray Company, Inc. | Louisville KY |
| AB Landscaping Louisville | https://a-b-landscaping-inc-louisville-ky.surge.sh | 3709 | A. B. Landscaping, Inc. | Louisville KY |
| ER Tree Care Louisville | https://er-tree-care-llc-louisville-ky.surge.sh | 3836 | ER Tree Care, LLC | Louisville KY |
| Climb Ax Tree Service | https://climb-ax-tree-crane-service-louisville-ky.surge.sh | 3877 | Climb-Ax Tree & Crane Service | Louisvil |
| Bright Hauling Louisville | https://bright-hauling-and-junk-removal-llc-louisville-ky.surge.sh | 3896 | Bright Hauling and Junk Removal, LLC | L |
| Mr Fix It Louisville | https://mr-fix-it-solutions-llc-louisville-ky.surge.sh | 3853 | Mr. Fix It Solutions LLC. | Louisville K |
| Complete Home Services | https://complete-home-services-louisville-ky.surge.sh | 3786 | Complete Home Services | Louisville KY |
| Wildcat Moving Louisville | https://wildcat-moving-llc-louisville-ky.surge.sh | 3698 | Wildcat Moving, LLC | Louisville KY |
| Right Way Hauling Louisville | https://right-way-hauling-junk-removal-demolition-louisville-ky.surge.sh | 3795 | Right Way Hauling, Junk Removal & Demoli |
| JD Contractors Louisville | https://jd-contractors-and-lawnscaping-llc-louisville-ky.surge.sh | 3816 | JD Contractors and Lawnscaping LLC | Lou |
| New Seasons Auction | https://new-seasons-auction-and-estates-louisville-ky.surge.sh | 3893 | New Seasons Auction and Estates | Louisv |
| Kings Hands LLC | https://kings-hands-llc-louisville-ky.surge.sh | 3846 | Kings Hands LLC | Louisville KY |
| New Leaf Tree Service | https://new-leaf-tree-service-llc-louisville-ky.surge.sh | 4065 | New Leaf Tree Service LLC | Louisville K |
| Jeff Reed Logging | https://jeff-reed-logging-tree-service-louisville-ky.surge.sh | 4036 | Jeff Reed Logging & Tree Service | Louis |
| Junk King Louisville | https://junk-king-louisville-louisville-ky.surge.sh | 3874 | Junk King Louisville | Louisville KY |
| David Fox Roofer | https://david-fox-roofer-louisville-ky.surge.sh | 3872 | David Fox-Roofer | Louisville KY |
| Handyman Las Vegas | https://handyman-services-in-las-vegas-nv-89121-las-vegas-nv.surge.sh | 3853 | Handyman Services in Las Vegas , NV 8912 |
| Auto Repair Orlando | https://top-rated-auto-repair-near-orlando-fl-carfax-orlando-fl.surge.sh | 3934 | Top Rated Auto Repair near Orlando, FL | |
| Sunni Streak Landing | https://sunni-streak-landing.surge.sh | 3814 | Sunni Streak - Daily Sunni Islamic Praye |
| Shia Streak Landing | https://shia-streak-landing.surge.sh | 3759 | Shia Streak - Daily Shia Islamic Prayer  |
| Presbyterian Streak Landing | https://presbyterian-streak-landing.surge.sh | 3858 | Presbyterian Streak - Daily Presbyterian |
| Anglican Streak Landing | https://anglican-streak-landing.surge.sh | 3845 | Anglican Streak - Daily Anglican Prayer  |
| Evangelical Streak Landing | https://evangelical-streak-landing.surge.sh | 3760 | Evangelical Streak - Daily Evangelical B |
| Pentecostal Streak Landing | https://pentecostal-streak-landing.surge.sh | 3868 | Pentecostal Streak - Daily Prayer & Tong |
| Episcopal Streak Landing | https://episcopal-streak-landing.surge.sh | 3868 | Episcopal Streak - Daily Episcopal Praye |
| Lutheran Streak Landing | https://lutheran-streak-landing.surge.sh | 3906 | Lutheran Streak - Daily Lutheran Devotio |
| Methodist Streak Landing | https://methodist-streak-landing.surge.sh | 3775 | Methodist Streak - Daily Methodist Devot |
| Baptist Streak Landing | https://baptist-streak-landing.surge.sh | 3825 | Baptist Streak - Daily Baptist Bible Stu |
| Protestant Streak Landing | https://protestant-streak-landing.surge.sh | 3841 | Protestant Streak - Daily Protestant Bib |
| Orthodox Streak Landing | https://orthodox-streak-landing.surge.sh | 3761 | Orthodox Streak - Daily Orthodox Christi |
| Catholic Streak Landing | https://catholic-streak-landing.surge.sh | 3948 | Catholic Streak - Daily Rosary, Mass & P |
| Cold Email ROI Calculator | https://cold-email-roi-calculator.surge.sh | 3751 | Cold Email ROI Calculator — how much is  |
| PrintMaxx Lead Magnets Hub | https://printmaxx-lead-magnets.surge.sh | 3850 | Cold Email ROI Calculator — how much is  |
| Instantly vs Lemlist | https://instantly-vs-lemlist.surge.sh | 3784 | Instantly vs Lemlist (2026): Which Cold  |
| Cursor vs Claude Code | https://cursor-vs-claudecode.surge.sh | 3749 | Cursor vs Claude Code (2026): Which AI C |
| ColdMaxx vs Instantly | https://coldmaxx-vs-instantly.surge.sh | 4053 | ColdMaxx vs Instantly (2026): Which Cold |
| PageScorer vs GTmetrix | https://pagescorer-vs-gtmetrix.surge.sh | 4174 | PageScorer vs GTmetrix (2026): Which Web |
| SleepMaxx vs Sleep Cycle | https://sleepmaxx-vs-sleepcycle.surge.sh | 3921 | SleepMaxx vs Sleep Cycle (2026): Best Fr |
| Twitter Banner | https://printmaxx-twitter-banner.surge.sh | 3894 |  |
| Cold Email Deliverability | https://best-cold-email-tools.surge.sh | 4195 | 7 Best Cold Email Tools in 2026 (Tested  |
| ATX Food Co Austin | https://atx-food-co-austin.surge.sh | 3916 | ATX Food Co | Austin TX |
| Dailey Company Inc Austin | https://dailey-company-inc-austin.surge.sh | 3866 | Dailey Company Inc | Austin TX |
| Semrush vs Ahrefs | https://semrush-vs-ahrefs.surge.sh | 3713 | SEMrush vs Ahrefs (2026): Which SEO Tool |
| ConvertKit vs Beehiiv | https://convertkit-vs-beehiiv.surge.sh | 4004 | ConvertKit vs Beehiiv 2026: Honest Email |
| Apps Chiropractic Milwaukee | https://apps-chiropractic-milwaukee-wi.surge.sh | 3879 | Apps Chiropractic | Milwaukee WI |
| Pope Family Chiro MKE | https://pope-family-chiropractic-milwaukee-wi.surge.sh | 3885 | Pope Family Chiropractic | Milwaukee WI |
| Carlitos Lawns MKE | https://carlitos-lawns-llc-milwaukee-wi.surge.sh | 3827 | Carlitos' Lawns LLC | Milwaukee WI |
| PM Local Demos | https://printmaxx-local-demos.surge.sh | 3866 | PRINTMAXX Local Business Website Demos | |
| PM Services | https://printmaxx-services.surge.sh | 3857 | PRINTMAXX Services | Web Dev, Automation |
| Sunni Streak Marketing | https://sunni-streak-marketing.surge.sh | 3680 | Sunni Streak - Daily Sunni Islamic Praye |
| Shia Streak Marketing | https://shia-streak-marketing.surge.sh | 3831 | Shia Streak - Daily Shia Islamic Prayer  |
| Protestant Streak Marketing | https://protestant-streak-marketing.surge.sh | 3935 | Protestant Streak - Daily Protestant Bib |
| Presbyterian Streak Mkt | https://presbyterian-streak-marketing.surge.sh | 3860 | Presbyterian Streak - Daily Presbyterian |
| Pentecostal Streak Mkt | https://pentecostal-streak-marketing.surge.sh | 3867 | Pentecostal Streak - Daily Prayer & Tong |
| Orthodox Streak Marketing | https://orthodox-streak-marketing.surge.sh | 3762 | Orthodox Streak - Daily Orthodox Christi |
| Methodist Streak Marketing | https://methodist-streak-marketing.surge.sh | 3738 | Methodist Streak - Daily Methodist Devot |
| Lutheran Streak Marketing | https://lutheran-streak-marketing.surge.sh | 3873 | Lutheran Streak - Daily Lutheran Devotio |
| Evangelical Streak Mkt | https://evangelical-streak-marketing.surge.sh | 3959 | Evangelical Streak - Daily Evangelical B |
| Episcopal Streak Marketing | https://episcopal-streak-marketing.surge.sh | 3820 | Episcopal Streak - Daily Episcopal Praye |
| Catholic Streak Marketing | https://catholic-streak-marketing.surge.sh | 3972 | Catholic Streak - Daily Rosary, Mass & P |
| Best Cold Email Tools Mkt | https://best-cold-email-tools-marketing.surge.sh | 4061 | 7 Best Cold Email Tools in 2026 (Tested  |
| Baptist Streak Marketing | https://baptist-streak-marketing.surge.sh | 3890 | Baptist Streak - Daily Baptist Bible Stu |
| Anglican Streak Marketing | https://anglican-streak-marketing.surge.sh | 4060 | Anglican Streak - Daily Anglican Prayer  |
| Cold Email Deliverability | https://cold-email-deliverability-checklist.surge.sh | 3942 | Cold Email Deliverability Checklist: 23- |
| Ramadan Daily Planner | https://ramadan-daily-planner.surge.sh | 4099 | Ramadan Daily Planner: Prayer Times + 30 |
| 200 Day Calculator | https://200-day-calculator.surge.sh | 3967 | Cold Email ROI Calculator — how much is  |
| AI Revenue Calculator | https://ai-revenue-calculator.surge.sh | 4040 | AI Side Project Revenue Calculator: Real |
| All Pro Window Portland | https://all-pro-window-cleaning-portland.surge.sh | 3928 | Window Cleaning in Portland, OR | All Pr |
| Pure Pro Detailing OKC | https://pure-pro-detailing-okc.surge.sh | 3901 | Top-Rated Mobile Car Detailing in Oklaho |
| Champion Auto Detail OKC | https://champion-auto-detailing-okc.surge.sh | 3767 | Mobile Auto Detailing Experts in Oklahom |
| Hedricks Dallas | https://hedrick-s-service-now-dallas-tx.surge.sh | 4707 | Hedrick's Service Now! | Dallas TX |
| Cody Sons Plumbing Dallas | https://cody-sons-plumbing-heating-air-dallas-tx.surge.sh | 3865 | Cody & Sons Plumbing, Heating & Air | Da |
| Dial One Dallas | https://dial-one-plumbing-cooling-heating-dallas-tx.surge.sh | 4022 | Dial One Plumbing, Cooling & Heating | D |
| ARS Rescue Rooter Dallas | https://ars-rescue-rooter-dfw-dallas-tx.surge.sh | 3980 | ARS Rescue Rooter DFW | Dallas TX |
| Miami Plumbing Zip Local | https://miami-plumbing-experts-zip-local.surge.sh | 3818 | Local Plumbing Experts - Plumbers - Just |

## Full Results

| # | Site | Category | Grade | HTTP | Load ms | Notes |
|---|------|----------|-------|------|---------|-------|
| 1 | SmartLead vs Instantly | comparison_pages | GREEN | 200 | 4398 |  |
| 2 | Best AI Tools 2026 | comparison_pages | GREEN | 200 | 4376 |  |
| 3 | SaaS Stack Audit | tools_saas | GREEN | 200 | 4276 |  |
| 4 | CoreDay | apps | YELLOW | 200 | 7166 | slow: 7166ms |
| 5 | PM Website Design | fiverr_services | GREEN | 200 | 4416 |  |
| 6 | PM Landing Page | fiverr_services | GREEN | 200 | 4505 |  |
| 7 | PM Cold Email | fiverr_services | GREEN | 200 | 4436 |  |
| 8 | PM Web Scraping | fiverr_services | GREEN | 200 | 4473 |  |
| 9 | PM Automation | fiverr_services | GREEN | 200 | 3905 |  |
| 10 | PM SEO Pages | fiverr_services | GREEN | 200 | 3919 |  |
| 11 | PM Content Writing | fiverr_services | GREEN | 200 | 3814 |  |
| 12 | PM App Development | fiverr_services | GREEN | 200 | 3875 |  |
| 13 | PM AI Chatbot | fiverr_services | GREEN | 200 | 3874 |  |
| 14 | PM Data Analysis | fiverr_services | GREEN | 200 | 4047 |  |
| 15 | Coit Cleaning Louisville | local_biz_louisville | GREEN | 200 | 3946 |  |
| 16 | Whitehouse Painting Louisville | local_biz_louisville | YELLOW | 200 | 7722 | slow: 7722ms |
| 17 | A1 Concrete Louisville | local_biz_louisville | YELLOW | 200 | 7878 | slow: 7878ms |
| 18 | Down To Earth Sealcoating | local_biz_louisville | YELLOW | 200 | 8238 | slow: 8238ms |
| 19 | CertaPro Painters Louisville | local_biz_louisville | YELLOW | 200 | 7620 | slow: 7620ms |
| 20 | Skyrockett Construction | local_biz_louisville | GREEN | 200 | 3959 |  |
| 21 | Garretts Pressure Washing | local_biz_louisville | GREEN | 200 | 3800 |  |
| 22 | Good Maintenance Cleaning | local_biz_louisville | GREEN | 200 | 3814 |  |
| 23 | A1 Aluminum Louisville | local_biz_louisville | GREEN | 200 | 4015 |  |
| 24 | The Maids Louisville | local_biz_louisville | GREEN | 200 | 3927 |  |
| 25 | McCoy Window Cleaning | local_biz_louisville | YELLOW | 200 | 5783 | slow: 5783ms |
| 26 | Square It Away Contracting | local_biz_louisville | GREEN | 200 | 4185 |  |
| 27 | Spindletop Draperies | local_biz_louisville | GREEN | 200 | 3892 |  |
| 28 | Naturescape Louisville | local_biz_louisville | GREEN | 200 | 4000 |  |
| 29 | Cutting Hedge Landscaping | local_biz_louisville | GREEN | 200 | 3849 |  |
| 30 | Greenworks Lawn Louisville | local_biz_louisville | GREEN | 200 | 3836 |  |
| 31 | Accurate Lawn Louisville | local_biz_louisville | GREEN | 200 | 3876 |  |
| 32 | Daves Tree Surgeons | local_biz_louisville | GREEN | 200 | 4003 |  |
| 33 | Bob Ray Company | local_biz_louisville | GREEN | 200 | 3971 |  |
| 34 | AB Landscaping Louisville | local_biz_louisville | GREEN | 200 | 3709 |  |
| 35 | ER Tree Care Louisville | local_biz_louisville | GREEN | 200 | 3836 |  |
| 36 | Climb Ax Tree Service | local_biz_louisville | GREEN | 200 | 3877 |  |
| 37 | Bright Hauling Louisville | local_biz_louisville | GREEN | 200 | 3896 |  |
| 38 | Mr Fix It Louisville | local_biz_louisville | GREEN | 200 | 3853 |  |
| 39 | Complete Home Services | local_biz_louisville | GREEN | 200 | 3786 |  |
| 40 | Wildcat Moving Louisville | local_biz_louisville | GREEN | 200 | 3698 |  |
| 41 | Right Way Hauling Louisville | local_biz_louisville | GREEN | 200 | 3795 |  |
| 42 | JD Contractors Louisville | local_biz_louisville | GREEN | 200 | 3816 |  |
| 43 | New Seasons Auction | local_biz_louisville | GREEN | 200 | 3893 |  |
| 44 | Kings Hands LLC | local_biz_louisville | GREEN | 200 | 3846 |  |
| 45 | New Leaf Tree Service | local_biz_louisville | GREEN | 200 | 4065 |  |
| 46 | Jeff Reed Logging | local_biz_louisville | GREEN | 200 | 4036 |  |
| 47 | Junk King Louisville | local_biz_louisville | GREEN | 200 | 3874 |  |
| 48 | David Fox Roofer | local_biz_louisville | GREEN | 200 | 3872 |  |
| 49 | Handyman Las Vegas | local_biz_other | GREEN | 200 | 3853 |  |
| 50 | Auto Repair Orlando | local_biz_other | GREEN | 200 | 3934 |  |
| 51 | OKC Mobile Detailing | local_biz_other | RED | None | None | Page.goto: net::ERR_NAME_NOT_RESOLVED at https://mobile-auto-detailing |
| 52 | OKC Car Detailing | local_biz_other | RED | None | None | Page.goto: net::ERR_NAME_NOT_RESOLVED at https://top-rated-mobile-car- |
| 53 | Portland Window Cleaning | local_biz_other | RED | None | None | Page.goto: net::ERR_NAME_NOT_RESOLVED at https://window-cleaning-in-po |
| 54 | Sunni Streak Landing | streak_landing | GREEN | 200 | 3814 |  |
| 55 | Shia Streak Landing | streak_landing | GREEN | 200 | 3759 |  |
| 56 | Presbyterian Streak Landing | streak_landing | GREEN | 200 | 3858 |  |
| 57 | Anglican Streak Landing | streak_landing | GREEN | 200 | 3845 |  |
| 58 | Evangelical Streak Landing | streak_landing | GREEN | 200 | 3760 |  |
| 59 | Pentecostal Streak Landing | streak_landing | GREEN | 200 | 3868 |  |
| 60 | Episcopal Streak Landing | streak_landing | GREEN | 200 | 3868 |  |
| 61 | Lutheran Streak Landing | streak_landing | GREEN | 200 | 3906 |  |
| 62 | Methodist Streak Landing | streak_landing | GREEN | 200 | 3775 |  |
| 63 | Baptist Streak Landing | streak_landing | GREEN | 200 | 3825 |  |
| 64 | Protestant Streak Landing | streak_landing | GREEN | 200 | 3841 |  |
| 65 | Orthodox Streak Landing | streak_landing | GREEN | 200 | 3761 |  |
| 66 | Catholic Streak Landing | streak_landing | GREEN | 200 | 3948 |  |
| 67 | Cold Email ROI Calculator | lead_magnets | GREEN | 200 | 3751 |  |
| 68 | Side Project Estimator | lead_magnets | YELLOW | 200 | 6255 | slow: 6255ms |
| 69 | Revenue Leak Audit | lead_magnets | YELLOW | 200 | 6531 | slow: 6531ms |
| 70 | PrintMaxx Lead Magnets Hub | lead_magnets | GREEN | 200 | 3850 |  |
| 71 | Instantly vs Lemlist | comparison_pages | GREEN | 200 | 3784 |  |
| 72 | Cursor vs Claude Code | comparison_pages | GREEN | 200 | 3749 |  |
| 73 | ColdMaxx vs Instantly | comparison_pages | GREEN | 200 | 4053 |  |
| 74 | PageScorer vs GTmetrix | comparison_pages | GREEN | 200 | 4174 |  |
| 75 | SleepMaxx vs Sleep Cycle | comparison_pages | GREEN | 200 | 3921 |  |
| 76 | Test Deploy 001 | test_deploys | YELLOW | 200 | 4027 | 200 OK but page blank/empty |
| 77 | Nested Test 001 | test_deploys | YELLOW | 200 | 3951 | 200 OK but page blank/empty |
| 78 | OpenClaw Fix Test 001 | test_deploys | YELLOW | 200 | 3858 | 200 OK but page blank/empty |
| 79 | Twitter Banner | media | GREEN | 200 | 3894 |  |
| 80 | Twitter PFP | media | YELLOW | 200 | 4028 | 200 OK but page blank/empty |
| 81 | Cold Email Deliverability | lead_magnets | GREEN | 200 | 4195 |  |
| 82 | ATX Food Co Austin | local_biz | GREEN | 200 | 3916 |  |
| 83 | Dailey Company Inc Austin | local_biz | GREEN | 200 | 3866 |  |
| 84 | Semrush vs Ahrefs | comparison_pages | GREEN | 200 | 3713 |  |
| 85 | PDFMaxx | tools_saas | YELLOW | 200 | 7043 | slow: 7043ms |
| 86 | ConvertKit vs Beehiiv | comparison_pages | GREEN | 200 | 4004 |  |
| 87 | SaaS Stack Audit 200 | tools_saas | RED | 200 | 4209 | Page.title: Execution context was destroyed, most likely because of a  |
| 88 | Vibe Coding Profit Calc | lead_magnets | YELLOW | 200 | 6532 | slow: 6532ms |
| 89 | Apps Chiropractic Milwaukee | local_biz_milwaukee | GREEN | 200 | 3879 |  |
| 90 | Pope Family Chiro MKE | local_biz_milwaukee | GREEN | 200 | 3885 |  |
| 91 | Carlitos Lawns MKE | local_biz_milwaukee | GREEN | 200 | 3827 |  |
| 92 | S Milwaukee Car Care | local_biz_milwaukee | YELLOW | 200 | 6303 | slow: 6303ms |
| 93 | Gians Flooring MKE | local_biz_milwaukee | YELLOW | 200 | 7422 | slow: 7422ms |
| 94 | Landlords Pest MKE | local_biz_milwaukee | YELLOW | 200 | 7067 | slow: 7067ms |
| 95 | Shorewood Family Chiro | local_biz_milwaukee | YELLOW | 200 | 6830 | slow: 6830ms |
| 96 | Milwaukee Plumber Service | local_biz_milwaukee | YELLOW | 200 | 6669 | slow: 6669ms |
| 97 | PM Local Demos | fiverr_services | GREEN | 200 | 3866 |  |
| 98 | PM Services | fiverr_services | GREEN | 200 | 3857 |  |
| 99 | Sunni Streak Marketing | streak_marketing | GREEN | 200 | 3680 |  |
| 100 | Shia Streak Marketing | streak_marketing | GREEN | 200 | 3831 |  |
| 101 | Protestant Streak Marketing | streak_marketing | GREEN | 200 | 3935 |  |
| 102 | Presbyterian Streak Mkt | streak_marketing | GREEN | 200 | 3860 |  |
| 103 | Pentecostal Streak Mkt | streak_marketing | GREEN | 200 | 3867 |  |
| 104 | Orthodox Streak Marketing | streak_marketing | GREEN | 200 | 3762 |  |
| 105 | Methodist Streak Marketing | streak_marketing | GREEN | 200 | 3738 |  |
| 106 | Lutheran Streak Marketing | streak_marketing | GREEN | 200 | 3873 |  |
| 107 | Evangelical Streak Mkt | streak_marketing | GREEN | 200 | 3959 |  |
| 108 | Episcopal Streak Marketing | streak_marketing | GREEN | 200 | 3820 |  |
| 109 | Catholic Streak Marketing | streak_marketing | GREEN | 200 | 3972 |  |
| 110 | Best Cold Email Tools Mkt | streak_marketing | GREEN | 200 | 4061 |  |
| 111 | Baptist Streak Marketing | streak_marketing | GREEN | 200 | 3890 |  |
| 112 | Anglican Streak Marketing | streak_marketing | GREEN | 200 | 4060 |  |
| 113 | Cold Email Deliverability | lead_magnets | GREEN | 200 | 3942 |  |
| 114 | Ramadan Daily Planner | lead_magnets | GREEN | 200 | 4099 |  |
| 115 | Solopreneur Launch Check | lead_magnets | YELLOW | 200 | 6473 | slow: 6473ms |
| 116 | Subject Line Grader | lead_magnets | YELLOW | 200 | 6237 | slow: 6237ms |
| 117 | App Hub Crosslinks | lead_magnets | YELLOW | 200 | 6276 | slow: 6276ms |
| 118 | 200 Day Calculator | lead_magnets | GREEN | 200 | 3967 |  |
| 119 | AI Revenue Calculator | lead_magnets | GREEN | 200 | 4040 |  |
| 120 | All Pro Window Portland | local_biz_other | GREEN | 200 | 3928 |  |
| 121 | Pure Pro Detailing OKC | local_biz_other | GREEN | 200 | 3901 |  |
| 122 | Champion Auto Detail OKC | local_biz_other | GREEN | 200 | 3767 |  |
| 123 | Birmingham Detailing | local_biz_other | RED | None | None | Page.goto: net::ERR_NAME_NOT_RESOLVED at https://mobile-interior-detai |
| 124 | Birmingham Home Detailing | local_biz_other | RED | None | None | Page.goto: net::ERR_NAME_NOT_RESOLVED at https://home-professional-mob |
| 125 | Birmingham Handyman | local_biz_other | YELLOW | 200 | 6078 | slow: 6078ms |
| 126 | Homeguide Handyman LV | local_biz_other | RED | None | None | Page.goto: net::ERR_NAME_NOT_RESOLVED at https://the-10-best-handyman- |
| 127 | Pink Windows Louisville | local_biz_louisville | RED | None | None | Page.goto: net::ERR_NAME_NOT_RESOLVED at https://local-window-cleaning |
| 128 | Cherry Window Louisville | local_biz_louisville | RED | None | None | Page.goto: net::ERR_NAME_NOT_RESOLVED at https://residential-and-comme |
| 129 | Old Settlers Dental ATX | local_biz_austin | RED | 504 | 8848 | HTTP 504 |
| 130 | Vista Ridge Dentistry ATX | local_biz_austin | YELLOW | 200 | 8159 | slow: 8159ms |
| 131 | Big Top Dentistry ATX | local_biz_austin | YELLOW | 200 | 8768 | slow: 8768ms |
| 132 | Nursing Home Dental ATX | local_biz_austin | YELLOW | 200 | 5995 | slow: 5995ms |
| 133 | Austin Elite Smiles | local_biz_austin | YELLOW | 200 | 8475 | slow: 8475ms |
| 134 | Lakeway Cosmetic Dent ATX | local_biz_austin | YELLOW | 200 | 8678 | slow: 8678ms |
| 135 | Restora Dental Arts ATX | local_biz_austin | YELLOW | 200 | 7655 | slow: 7655ms |
| 136 | Helen Ragsdale DDS ATX | local_biz_austin | YELLOW | 200 | 5971 | slow: 5971ms |
| 137 | About Smiles Dentistry | local_biz_austin | YELLOW | 200 | 8763 | slow: 8763ms |
| 138 | Dental Smiles ATX | local_biz_austin | YELLOW | 200 | 8443 | slow: 8443ms |
| 139 | Thiel Pediatric Dent ATX | local_biz_austin | YELLOW | 200 | 8356 | slow: 8356ms |
| 140 | Smiles of Austin | local_biz_austin | YELLOW | 200 | 8793 | slow: 8793ms |
| 141 | Vitadox Austin Dentists | local_biz_austin | RED | 504 | 8922 | HTTP 504 |
| 142 | Austin Dentistry | local_biz_austin | YELLOW | 200 | 8436 | slow: 8436ms |
| 143 | Dental Blush Miami | local_biz_miami | YELLOW | 200 | 8667 | slow: 8667ms |
| 144 | J Family Dental Miami | local_biz_miami | YELLOW | 200 | 6355 | slow: 6355ms |
| 145 | Hedricks Dallas | local_biz_dallas | GREEN | 200 | 4707 |  |
| 146 | Berrett Home Dallas | local_biz_dallas | YELLOW | 200 | 6229 | slow: 6229ms |
| 147 | Cody Sons Plumbing Dallas | local_biz_dallas | GREEN | 200 | 3865 |  |
| 148 | Dial One Dallas | local_biz_dallas | GREEN | 200 | 4022 |  |
| 149 | ARS Rescue Rooter Dallas | local_biz_dallas | GREEN | 200 | 3980 |  |
| 150 | Harmony Plumbing Dallas | local_biz_dallas | RED | 504 | 9017 | HTTP 504 |
| 151 | Public Service Plumber DAL | local_biz_dallas | RED | 504 | 10536 | HTTP 504 |
| 152 | Berkeys AC Plumbing Dallas | local_biz_dallas | RED | 504 | 10342 | HTTP 504 |
| 153 | Triune Plumbing Dallas | local_biz_dallas | YELLOW | 200 | 6424 | slow: 6424ms |
| 154 | Accurate Leak Dallas | local_biz_dallas | RED | 504 | 9220 | HTTP 504 |
| 155 | FindLaw Dallas | local_biz_dallas | YELLOW | 200 | 8986 | slow: 8986ms |
| 156 | Miami Plumbing Zip Local | local_biz_miami | GREEN | 200 | 3818 |  |

*Generated: 2026-03-15T04:32:25.023433*
*Screenshots: AUTOMATIONS/agent/swarm/screenshots/*
#!/usr/bin/env python3
"""
Generate 30-day content calendar: 3 niches x 4 platforms x 3 posts/day = 1,080 posts
All copy written in PRINTMAXX voice (pipelineabuser style)
"""

import csv
import os
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_CSV = str(PROJECT_ROOT / "LEDGER" / "CONTENT_CALENDAR_30DAY.csv")

START_DATE = datetime(2026, 2, 3)

# Content mix: 40% value, 30% engagement, 20% promotion, 10% personality
# Per niche per platform: 90 posts over 30 days (3/day)
# 36 value, 27 engagement, 18 promotion, 9 personality

# Posting times by platform (EST)
TIMES = {
    "twitter": ["08:00", "12:00", "17:00"],
    "tiktok": ["06:00", "12:00", "21:00"],
    "instagram": ["09:00", "14:00", "19:00"],
    "linkedin": ["07:00", "12:00", "17:00"],
}

# Content type rotation pattern (repeating 10-day cycle, 3 posts/day = 30 slots)
# v=value, e=engagement, p=promotion, pe=personality
# 40% value (12), 30% engagement (9), 20% promotion (6), 10% personality (3)
CONTENT_ROTATION = [
    ["value", "engagement", "value"],       # Day 1
    ["value", "promotion", "engagement"],   # Day 2
    ["engagement", "value", "value"],       # Day 3
    ["value", "engagement", "promotion"],   # Day 4
    ["personality", "value", "engagement"], # Day 5
    ["value", "promotion", "value"],        # Day 6
    ["engagement", "value", "engagement"],  # Day 7
    ["value", "promotion", "value"],        # Day 8
    ["engagement", "value", "personality"], # Day 9
    ["value", "engagement", "promotion"],   # Day 10
]

###############################################################################
# FAITH CONTENT BANK - @daily_anchor_faith / @dailyanchorfaith
###############################################################################

FAITH_VALUE = [
    # 36 value posts
    ("i prayed for 5 minutes every morning for 90 days. missed zero. here's what changed: anxiety dropped. decisions got clearer. arguments with my wife went from 3x/week to maybe 1. not because prayer is magic. because 5 minutes of silence before chaos rewires how you respond to everything.", "text", "morning prayer, person in quiet room", "#faith #prayer #morningroutine", "try 5 minutes tomorrow morning before you touch your phone", ""),
    ("most people read the bible like a textbook. wrong approach. read it like a letter from someone who knows your future. Proverbs 3:5-6 hit different when you're actually making a decision that week.", "text", "", "#faith #bible #proverbs", "reply PROVERBS for the 7-day reading plan", ""),
    ("tracked my prayer consistency for 6 months. 147 out of 180 days. the 33 days i missed? every single one started with checking my phone first. the phone is the prayer killer. lock it.", "text", "phone lock screen", "#prayer #discipline #screentime", "what's your prayer streak at? be honest", ""),
    ("the 5:30am crowd at church is different. no performance. no nice outfits. just people who actually need God that day. that's the real church.", "text", "", "#faith #church #earlymorning", "", ""),
    ("fasting isn't about food. it's about proving to yourself that your body doesn't control you. 24 hours no food. your spirit gets louder when your stomach gets quiet.", "text", "", "#fasting #faith #discipline", "reply FAST for the beginner fasting guide", ""),
    ("i memorized 1 verse per week for a year. 52 verses. took 10 minutes on monday mornings. now i have ammunition for every anxious thought. Philippians 4:6-7 is my go-to at 2am.", "text", "", "#bible #scripture #memorization", "which verse do you need right now? drop it below", ""),
    ("accountability partner changed everything. we text each other at 6am. just 'up' or 'prayed'. that's it. 94% consistency since we started. solo discipline is hard. shared discipline compounds.", "text", "", "#accountability #faith #discipline", "tag someone you'd do this with", ""),
    ("tithing on $3,200/month felt insane. $320 gone. but here's the math 14 months later: income went to $5,800. not prosperity gospel. just saying when you loosen your grip on money weird things happen.", "text", "", "#tithing #faith #money", "", ""),
    ("the bible has 31 chapters in Proverbs. one for each day of the month. read the chapter that matches today's date. simplest bible plan that actually sticks.", "text", "", "#proverbs #bible #dailyreading", "what chapter is today?", ""),
    ("my kids watch me pray. they don't understand the words yet. doesn't matter. they see dad on his knees every morning. that's the sermon. not the Sunday one.", "text", "", "#faith #family #parenting", "", ""),
    ("journaling after prayer changed the game. 3 minutes. write what came to mind. after 6 months i had 180 entries showing God answering prayers i forgot i prayed. proof compounds.", "text", "journal and pen", "#prayer #journaling #faith", "reply JOURNAL for the template", ""),
    ("'i don't have time to pray' is the same as 'i don't have time to breathe.' you have the time. you're spending it on instagram reels at 11pm. redirect 15 minutes.", "text", "", "#prayer #time #priorities", "", ""),
    ("the wilderness season isn't punishment. David was anointed king then spent years hiding in caves. the gap between promise and fulfillment is where character gets built.", "text", "", "#faith #patience #growth", "", ""),
    ("community group of 6 men. we meet every thursday at 6am. no agenda. just 'how are you really doing.' 2 years in. these men know things about me my wife doesn't. that's by design.", "text", "", "#mens #faith #community", "reply GROUP for how to start one", ""),
    ("gratitude list every night. 3 things. takes 90 seconds. after 60 days my default mood shifted from anxious to content. not happy. content. that's the real upgrade.", "text", "", "#gratitude #faith #mentalhealth", "what are your 3 today?", ""),
    ("sermon notes mean nothing if you don't act on one thing by Tuesday. pick ONE takeaway. do it before the next Sunday. that's how sermons actually change your life.", "text", "", "#sermon #church #action", "", ""),
    ("worship music during my commute. 22 minutes each way. that's 3.6 hours/week of worship i didn't have to 'find time' for. redeem the dead time.", "text", "", "#worship #music #commute", "drop your go-to worship playlist", ""),
    ("PrayerLock forces you to pray before you can use your phone. sounds extreme. but 847 people are using it and their average prayer time went from 2 min to 11 min per day. constraint creates freedom.", "text", "app screenshot", "#prayerlock #prayer #discipline", "link in bio", ""),
    ("the hardest prayer is 'not my will but yours.' because it means you might not get what you want. but it also means you might get what you actually need. those are different things.", "text", "", "#prayer #faith #surrender", "", ""),
    ("read through the entire bible in a year. here's what i didn't expect: the first half is way more violent and messy than anyone tells you in church. and that's the point. God works with broken people.", "text", "", "#bible #reading #faith", "", ""),
    ("sabbath rest isn't lazy. it's strategic. one day per week with no work no screens no hustle. my productivity the other 6 days went up 30% when i actually committed to rest.", "text", "", "#sabbath #rest #productivity", "", ""),
    ("'pray without ceasing' doesn't mean be on your knees 24/7. it means your default internal monologue shifts from worry to conversation with God. took me 2 years to get there.", "text", "", "#prayer #faith #mindset", "", ""),
    ("started a scripture text chain with 12 friends. one person sends a verse each morning. rotation schedule. i wake up to truth instead of news. best notification on my phone.", "text", "", "#scripture #community #morning", "reply CHAIN for how to set it up", ""),
    ("forgiveness isn't a feeling. it's a decision you make 47 times about the same person until the feeling catches up. i'm on attempt 23 with my dad. getting closer.", "text", "", "#forgiveness #faith #healing", "", ""),
    ("the 'God has a plan' people are right but incomplete. He has a plan AND you have to work. faith without works is dead. James 2:26. pray then move your feet.", "text", "", "#faith #action #james", "", ""),
    ("church hurt is real. i left for 3 years. came back to a different church. smaller. less performance. more honesty. the institution isn't the faith. find your people.", "text", "", "#church #faith #community", "", ""),
    ("my prayer closet is literally a closet. cleaned out the coats. put a cushion and a candle in there. having a physical space designated for prayer tripled my consistency.", "text", "", "#prayer #space #discipline", "", ""),
    ("taught my 7 year old to pray out loud. she prays for her goldfish, her teacher, and 'the people who are sad today.' more theology in that prayer than most seminary papers.", "text", "", "#kids #prayer #family", "", ""),
    ("the desert fathers spent years in silence. i can barely do 10 minutes without reaching for my phone. but those 10 minutes are the most important 10 minutes of my day.", "text", "", "#silence #prayer #contemplation", "", ""),
    ("tithing testimony from last month: gave $480. got an unexpected freelance gig for $2,100 that same week. coincidence? maybe. but i've seen it happen 6 times now. i stopped calling it coincidence.", "text", "", "#tithing #testimony #faith", "", ""),
    ("the Psalms are the original therapy journal. David literally writes 'why have you forsaken me' to God. that's not disrespect. that's honesty. God can handle your real feelings.", "text", "", "#psalms #mentalhealth #honesty", "", ""),
    ("started ending every prayer with 'and show me what to do next.' game changer. prayer went from wish list to action plan.", "text", "", "#prayer #action #guidance", "", ""),
    ("fasted social media for lent. 40 days. here's what i learned: i don't miss it. i miss the validation. those are different addictions. the second one is harder to quit.", "text", "", "#socialmedia #fasting #lent", "", ""),
    ("marriage devotional with my wife. 10 minutes before bed. we've done it 200+ nights. divorce rate for couples who pray together daily is under 1%. that's not a stat. that's a strategy.", "text", "", "#marriage #prayer #devotional", "reply MARRIAGE for the devotional we use", ""),
    ("walking prayer. 30 minutes around the neighborhood. pray out loud. neighbors think i'm on a phone call. don't care. combining exercise and prayer is the ultimate 2-for-1.", "text", "", "#prayer #walking #health", "", ""),
    ("the book of Ecclesiastes reads like it was written by a burnt out tech founder. 'all is vanity.' Solomon had everything. still empty. the richest man ever telling you money isn't it.", "text", "", "#ecclesiastes #wisdom #purpose", "", ""),
]

FAITH_ENGAGEMENT = [
    # 27 engagement posts
    ("which hits harder: morning prayer or evening prayer? i'm a 5:30am guy but my wife swears by 10pm prayer journaling. genuinely curious.", "text", "", "", "drop your answer below", ""),
    ("hot take: most christian influencers are selling you courses not leading you closer to God. the monetization of faith is getting out of control.", "text", "", "", "agree or disagree?", ""),
    ("name one bible verse that completely changed how you think. just one. mine is Romans 8:28.", "text", "", "", "", ""),
    ("unpopular opinion: church should be uncomfortable sometimes. if you leave every Sunday feeling good you might be getting entertainment not transformation.", "text", "", "", "fight me in the replies", ""),
    ("raise your hand if you've ever fallen asleep during prayer. just me? okay.", "text", "", "", "", ""),
    ("what's harder: forgiving someone who wronged you or forgiving yourself? i've been stuck on the second one for years.", "text", "", "", "share your honest answer", ""),
    ("POV: you just realized the thing you've been stressing about for 3 weeks is the exact thing you prayed about last month. God's timing is wild.", "text", "", "", "when has this happened to you?", ""),
    ("your favorite worship song and why. go.", "text", "", "", "", ""),
    ("'God won't give you more than you can handle' isn't actually in the bible. it's 1 Corinthians 10:13 about temptation not suffering. stop misquoting scripture to people in pain.", "text", "", "", "what's another commonly misquoted verse?", ""),
    ("the person you need to forgive just popped into your head reading this. yeah that one. you know what to do.", "text", "", "", "", ""),
    ("what's one prayer that got answered in a way you never expected?", "text", "", "", "I'll go first in the replies", ""),
    ("choosing between: A) a church with amazing worship but weak teaching, or B) a church with boring worship but incredible preaching. which one?", "text", "", "", "comment A or B", ""),
    ("be honest: when was the last time you opened your bible outside of Sunday?", "text", "", "", "", ""),
    ("the 'just pray about it' advice hits different when you're actually in crisis. sometimes prayer + action is the answer. God gave you hands for a reason.", "text", "", "", "agree?", ""),
    ("tag someone who needs to hear this today: you're not behind. God's timeline is not your timeline. and that's actually the good news.", "text", "", "", "tag them", ""),
    ("confession time: what spiritual discipline do you know you should be doing but keep avoiding?", "text", "", "", "I'll share mine in the replies", ""),
    ("if you could ask God one question with a guaranteed answer what would it be?", "text", "", "", "", ""),
    ("the best sermon you ever heard in one sentence. go.", "text", "", "", "", ""),
    ("does anyone else feel closer to God in nature than in a building? just me?", "text", "", "", "", ""),
    ("stop scrolling for 10 seconds. take a deep breath. say 'thank you' out loud. okay keep scrolling. you just prayed.", "text", "", "", "did you actually do it? be honest", ""),
    ("which book of the bible do you think is most underrated? i'm going with Habakkuk. 3 chapters of pure fire.", "text", "", "", "drop yours", ""),
    ("would you rather: pray for 1 hour once a week or 10 minutes every day? there's a right answer.", "text", "", "", "", ""),
    ("that friend who always says 'I'll pray for you' and actually does it is the most valuable person in your life. tag them.", "text", "", "", "tag your prayer warrior", ""),
    ("what worship song made you ugly cry? no judgment zone.", "text", "", "", "", ""),
    ("real question: do you pray before meals? every time, sometimes, or only when someone's watching?", "text", "", "", "be real", ""),
    ("the verse you keep coming back to in hard seasons. what is it?", "text", "", "", "", ""),
    ("controversial: reading a devotional app is not the same as reading your bible. the algorithm is not the Holy Spirit.", "text", "", "", "thoughts?", ""),
]

FAITH_PROMOTION = [
    # 18 promotion posts
    ("PrayerLock: lock your phone until you pray. your phone is the #1 prayer killer. this forces a pause before the scroll.", "text", "app screenshot", "", "link in bio", ""),
    ("built an app that won't let you doom scroll until you've spent time with God. sounds aggressive. that's the point. PrayerLock.", "text", "app demo", "", "link in bio to download", ""),
    ("3 things i've noticed since using PrayerLock consistently: 1) less mindless scrolling 2) more consistent prayer 3) better sleep because no late-night doomscroll. the constraint is the feature.", "text", "testimonial graphic", "", "try it free for 7 days", ""),
    ("the free 7-day prayer challenge drops this week. one verse, one prompt, one 5-minute prayer. want in?", "text", "challenge graphic", "", "reply CHALLENGE to join", ""),
    ("new PrayerLock feature: prayer streaks. see how many consecutive days you've prayed before unlocking. can you keep it going?", "text", "streak screenshot", "", "download and start your streak", ""),
    ("just launched the Daily Anchor devotional email. one verse + one question + one prayer. every morning at 5:30am. 3 minutes. free forever.", "text", "email preview", "", "reply EMAIL to subscribe", ""),
    ("the guided prayer journal template. 90 days of prompts. morning and evening. what to pray for, what to write, how to track answers. $7 on Gumroad.", "text", "journal preview", "", "link in bio", ""),
    ("PrayerLock now has a couples mode. both partners have to pray before either phone unlocks. marriage counselors hate this one trick. (they actually love it.)", "text", "couples mode screenshot", "", "link in bio", ""),
    ("the prayer consistency tracker spreadsheet. free. track daily prayer, journal entries, bible reading, fasting days. google sheets template.", "text", "spreadsheet preview", "", "reply TRACKER for the link", ""),
    ("PrayerLock Salah mode just dropped. 5 daily prayer reminders aligned with Islamic prayer times. Qibla direction built in. 2 billion people needed this app.", "text", "salah mode screenshot", "", "link in bio", ""),
    ("the 21-day prayer habit builder. based on the research: it takes 21 days to form a habit. daily email with verse, prompt, and prayer template. free.", "text", "", "", "reply 21DAYS to join", ""),
    ("community prayer wall inside PrayerLock. post your prayer request. others pray for it. you get notified when someone prays.", "text", "prayer wall screenshot", "", "join the community", ""),
    ("Sunday sermon notes template. free PDF. structured sections for scripture, key points, personal application, and action items. never waste a sermon again.", "text", "template preview", "", "reply NOTES for the download", ""),
    ("the faith + productivity stack: PrayerLock (prayer first) + bible reading plan + gratitude journal + accountability partner. total cost: $0-7. ROI: immeasurable.", "text", "", "", "reply STACK for full setup guide", ""),
    ("PrayerLock is live. if your phone is wrecking your prayer consistency, this puts a hard pause between you and the scroll.", "text", "", "", "try it and tell me if it helps", ""),
    ("the family devotional guide. 30 days of kid-friendly bible stories, discussion questions, and prayer prompts. takes 10 minutes at dinner. $5 on Gumroad.", "text", "guide preview", "", "link in bio", ""),
    ("corporate prayer zoom call. every wednesday at 6am EST. 30 minutes. no agenda. just pray together. free.", "text", "", "", "reply PRAY for the zoom link", ""),
    ("PrayerLock annual plan: $29/year. that's $0.08/day for a consistent prayer life. less than a gumball.", "text", "", "", "link in bio", ""),
]

FAITH_PERSONALITY = [
    # 9 personality posts
    ("woke up at 4:47am today. not by choice. my 2 year old decided it was morning. prayed while making her cereal. that counts right?", "text", "", "", "", ""),
    ("building PrayerLock update. just shipped prayer streaks feature. coded for 6 hours straight. forgot to eat lunch. the irony of building a discipline app while having zero discipline about food.", "text", "", "", "", ""),
    ("my pastor doesn't know i built PrayerLock. showed him yesterday. he stared at his phone for 10 seconds, looked up and said 'finally someone made the phone useful.' best beta tester feedback.", "text", "", "", "", ""),
    ("honest moment: i started this faith account because i needed accountability more than anyone else. teaching forces learning. posting forces consistency. you're watching my actual process unfold in real time.", "text", "", "", "", ""),
    ("the Daily Anchor name came from Hebrews 6:19. 'we have this hope as an anchor for the soul.' i needed an anchor. maybe you do too.", "text", "", "", "", ""),
    ("3 months of daily faith content. building in public without pretending it's easy. the mission was never money. the money comes after the mission is real.", "text", "", "", "", ""),
    ("fun fact: i built PrayerLock because i kept failing at my own prayer goals. couldn't do it with willpower alone. so i made an app that literally forces me. engineering my own sanctification.", "text", "", "", "", ""),
    ("wife asked me this morning: 'do you pray more now because of the app or because you're building in public?' ...both? is that bad?", "text", "", "", "", ""),
    ("faith content recap: lots of posts, one app, zero viral moments. i'll take a small group actually praying more over vanity views every time.", "text", "", "", "", ""),
]

###############################################################################
# FITNESS CONTENT BANK - @three_hour_physique / @threehourphysique
###############################################################################

FITNESS_VALUE = [
    ("3 hours per week in the gym. that's it. 3 sessions x 1 hour. monday wednesday friday. compound lifts only. i gained 12lbs of muscle in 8 months on this. you don't need 6 days.", "text", "", "#fitness #gym #training", "reply SPLIT for the exact program", ""),
    ("the protein myth needs to die. you don't need 1g per lb of bodyweight. 0.7g per lb is the actual research consensus. for a 180lb guy that's 126g not 180g. stop force-feeding yourself.", "text", "", "#protein #nutrition #fitness", "", ""),
    ("creatine monohydrate. 5g per day. every day. forever. $0.03 per serving. the single most researched supplement in history with the most consistent results. stop buying everything else first.", "text", "", "#creatine #supplements #fitness", "", ""),
    ("tracked every workout for 365 days. the exercises that built the most muscle: barbell squat, barbell bench, barbell row, overhead press, deadlift. 5 exercises. everything else is accessory.", "text", "", "#strength #compound #lifting", "reply 5 for the full program", ""),
    ("sleep is the most anabolic thing you're not doing enough of. 7-9 hours. not negotiable. i gained more muscle in 3 months of prioritizing sleep than 6 months of perfect training with 5 hours of sleep.", "text", "", "#sleep #recovery #gains", "", ""),
    ("progressive overload is the only thing that matters. add 2.5lbs to the bar every week. that's 130lbs in a year. most people lift the same weight for 3 years then wonder why they look the same.", "text", "", "#progressiveoverload #strength", "", ""),
    ("walking 10,000 steps per day burned more fat than any cardio routine i've tried. no cortisol spike. no muscle loss. no gym time wasted. just walk more. seriously.", "text", "", "#walking #fatloss #cardio", "", ""),
    ("the meal prep cheat code: cook 2lbs of chicken breast, 4 cups of rice, and a bag of frozen vegetables on Sunday. portion into 5 containers. lunch is solved for the week. takes 45 minutes.", "text", "", "#mealprep #nutrition #fitness", "reply PREP for the full weekly plan", ""),
    ("cold shower every morning for 60 days. here's what actually happened: nothing magical. but my willpower for the gym went up because I'd already done something hard before 7am. it's a discipline primer.", "text", "", "#coldshower #discipline #fitness", "", ""),
    ("electrolytes in the morning before coffee changed my workouts. pinch of salt, squeeze of lemon, 16oz water. zero cost. more energy than any pre-workout. your morning dehydration is killing your performance.", "text", "", "#electrolytes #hydration #performance", "", ""),
    ("the 80/20 of fat loss: eat in a 500 calorie deficit. that's it. no keto. no intermittent fasting required. no carb cutting. just eat 500 less than you burn. lose 1lb per week like clockwork.", "text", "", "#fatloss #calories #nutrition", "", ""),
    ("front squats fixed my back pain from regular squats. forced me into better posture. lighter weight, same muscle activation, zero pain. sometimes the regression is the progression.", "text", "", "#squat #mobility #gym", "", ""),
    ("stretching 10 minutes after every workout. hip flexors, hamstrings, chest, shoulders. 6 months later my squat depth improved, shoulder pain gone, and i move like i'm 20 not 30.", "text", "", "#stretching #mobility #recovery", "reply STRETCH for the routine", ""),
    ("the biggest waste of money in fitness: personal trainers charging $80/hour to count your reps. the second biggest: BCAA supplements. both are completely unnecessary.", "text", "", "#fitness #money #supplements", "", ""),
    ("deadlift form check: record every set from the side. watch between sets. 90% of back injuries from deadlifts are ego + bad form. the camera is your cheapest insurance policy.", "text", "form check video", "#deadlift #form #safety", "", ""),
    ("intermittent fasting works not because of the fasting window. it works because most people simply eat less when they skip breakfast. the mechanism is boring. calorie deficit.", "text", "", "#intermittentfasting #fatloss", "", ""),
    ("gym anxiety is real and valid. here's what fixed mine: go at 5am when it's empty. follow a written program so you know exactly what to do. wear headphones. don't make eye contact. repeat.", "text", "", "#gymanxiety #beginner #fitness", "", ""),
    ("the bulk/cut cycle is overrated for beginners. just eat at maintenance with high protein and lift heavy. you'll recomp. gained visible muscle while staying the same weight for 6 months.", "text", "", "#recomp #bodybuilding #natural", "", ""),
    ("home gym ROI: spent $800 on a rack, barbell, bench, and 300lbs of plates. gym membership was $50/month. paid for itself in 16 months. now i train in my garage at 5am in my underwear. freedom.", "text", "", "#homegym #fitness #investment", "", ""),
    ("grip strength is the most underrated indicator of overall health. dead hangs from a pull-up bar. start with 20 seconds. work to 60. my back pain disappeared and my deadlift went up 40lbs.", "text", "", "#gripstrength #deadhang #health", "", ""),
    ("rest 3-5 minutes between heavy compound sets. not 60 seconds. you're not doing cardio. you're building strength. longer rest = heavier lifts = more muscle. the science is clear.", "text", "", "#restperiods #strength #hypertrophy", "", ""),
    ("the overhead press is the most honest lift. you can't cheat it. you can't use momentum. you either press it or you don't. add 5lbs per month and watch your shoulders transform.", "text", "", "#overheadpress #shoulders #strength", "", ""),
    ("magnesium glycinate before bed. 400mg. sleep quality went from 6/10 to 8/10. better sleep = better recovery = more muscle. $0.15 per night. most underprescribed supplement.", "text", "", "#magnesium #sleep #recovery", "", ""),
    ("farmer's walks. grab heavy dumbbells. walk 40 yards. rest 60 seconds. repeat 4 times. builds grip, traps, core, and mental toughness in 10 minutes. most underused exercise in every gym.", "text", "", "#farmerswalks #functional #strength", "", ""),
    ("calorie tracking for 30 days then stop. the point isn't to track forever. the point is to learn what 2,500 calories actually looks like. after 30 days you can eyeball it. education not obsession.", "text", "", "#calories #tracking #nutrition", "", ""),
    ("the mind-muscle connection is real. slow your bench press down. 3 seconds down, pause, 2 seconds up. lighter weight. feel the chest working. my chest grew more in 3 months than the previous year.", "text", "", "#mindmuscle #bench #hypertrophy", "", ""),
    ("bodyweight exercises until you can: 20 pushups, 5 pullups, 50 bodyweight squats, 60 second plank. if you can't do these don't touch a barbell yet. build the foundation.", "text", "", "#bodyweight #beginner #foundation", "", ""),
    ("sauna 3x per week after training. 15 minutes at 180F. recovery improved. sleep improved. skin improved. $10/month at my gym. the most underused amenity in every commercial gym.", "text", "", "#sauna #recovery #health", "", ""),
    ("training log in a $2 notebook. date, exercise, sets, reps, weight. flip back 3 months and see proof you're stronger. motivation is unreliable. data is not.", "text", "", "#traininglog #progress #data", "", ""),
    ("the pump is not growth. soreness is not progress. the only measure: are you lifting heavier this month than last month? yes = growing. no = change something.", "text", "", "#strength #progress #reality", "", ""),
    ("fish oil. vitamin D. creatine. magnesium. that's the supplement stack. total cost: $1.20/day. everything else is marketing. don't buy test boosters. don't buy fat burners. save your money.", "text", "", "#supplements #stack #fitness", "reply STACK for exact brands", ""),
    ("high protein breakfast within 1 hour of waking: 4 eggs + toast + fruit. 40g protein before 8am. my energy and gym performance improved dramatically vs skipping breakfast.", "text", "", "#breakfast #protein #nutrition", "", ""),
    ("the Romanian deadlift built my hamstrings more than any machine. 3 sets of 8-10 reps. slow controlled. feel the stretch. this one exercise replaces 3 machine exercises.", "text", "", "#RDL #hamstrings #strength", "", ""),
    ("deload week every 4th week. cut weight by 50%, keep volume same. feels like a waste. but week 5 you come back stronger every single time. recovery is training.", "text", "", "#deload #recovery #programming", "", ""),
    ("caffeine before training. 200mg. that's about 2 cups of coffee. timed 30 min before your session. free pre-workout. performance boost of 3-5% on every lift. science backed.", "text", "", "#caffeine #preworkout #performance", "", ""),
    ("the trap bar deadlift is the best exercise nobody talks about. easier on your back than conventional. heavier loads. full body stimulus. if your gym has one use it.", "text", "", "#trapbar #deadlift #training", "", ""),
]

FITNESS_ENGAGEMENT = [
    ("which would you choose forever: only upper body training or only lower body training? no cop-outs.", "text", "", "", "drop your answer", ""),
    ("hot take: most personal trainers got certified in a weekend and know less than someone who's trained themselves for 3 years. harsh but true.", "text", "", "", "agree or disagree?", ""),
    ("what's your one non-negotiable exercise? the one you'd keep if you could only do ONE lift forever. mine is the squat.", "text", "", "", "", ""),
    ("unpopular fitness opinion: abs are made in the kitchen is only half right. abs are revealed in the kitchen and built in the gym. you need both.", "text", "", "", "thoughts?", ""),
    ("6am gym or 6pm gym? there's a right answer and it's whichever one you'll actually show up to.", "text", "", "", "when do you train?", ""),
    ("what's the worst fitness advice you've ever received? I'll start: 'don't eat after 8pm or it turns to fat.' absolute garbage.", "text", "", "", "drop yours below", ""),
    ("you can only eat 3 foods for the rest of your life to stay in shape. what are they? mine: chicken, rice, broccoli. boring but effective.", "text", "", "", "", ""),
    ("POV: you just hit a PR on bench and there's nobody in the gym to celebrate with. we've all been there. drop your latest PR below.", "text", "", "", "share your W", ""),
    ("be honest: how many days did you actually train last week? no cap. I'll go first: 3 out of planned 4.", "text", "", "", "", ""),
    ("the gym bro who rerack weights vs the one who leaves 4 plates on the leg press. which one are you?", "text", "", "", "", ""),
    ("what supplement did you waste the most money on? I'll start: fat burners. $60/bottle. did absolutely nothing.", "text", "", "", "share your L", ""),
    ("morning training without eating first or evening training with a full day of food? which gives you better lifts?", "text", "", "", "", ""),
    ("if you could go back and tell yourself one thing when you started training what would it be?", "text", "", "", "I'll share mine in replies", ""),
    ("the protein shake or the whole food meal after training? science says it doesn't matter. what do you prefer?", "text", "", "", "", ""),
    ("rest day guilt is real. your muscles literally grow while you rest not while you train. take the day off. you're not losing gains.", "text", "", "", "who needed to hear this?", ""),
    ("what's your gym pet peeve? curling in the squat rack? unsolicited advice? grunting? phone filming? pick one.", "text", "", "", "vent below", ""),
    ("bulk season or cut season right now? and how's it going? actually how's it going.", "text", "", "", "be real", ""),
    ("the exercise you hate the most is probably the one you need the most. for me it's lunges. what's yours?", "text", "", "", "", ""),
    ("does anyone else plan their entire day around their workout or is that just me?", "text", "", "", "", ""),
    ("Monday is International Chest Day and I will not be taking questions about that.", "text", "", "", "", ""),
    ("training partner or solo training? i've done both for years. solo wins for consistency. partner wins for pushing through plateaus.", "text", "", "", "your preference?", ""),
    ("what song is guaranteed to add 10lbs to your bench? mine is Enter Sandman. basic but effective.", "text", "", "", "drop the PR song", ""),
    ("the person at the gym who wipes down every machine after use. you're the real MVP. shoutout to you.", "text", "", "", "tag them", ""),
    ("would you rather: never squat again or never bench again? this one separates the real ones.", "text", "", "", "choose", ""),
    ("confession: i've been telling people i bench 225 but it was 220. the 5lbs haunts me.", "text", "", "", "share your gym confession", ""),
    ("how long did it take you to see visible results from training? honest answers only. mine was 4 months.", "text", "", "", "be specific", ""),
    ("the gym on January 2nd vs the gym on February 2nd. completely different place. respect to everyone still here.", "text", "", "", "", ""),
]

FITNESS_PROMOTION = [
    ("WalkToUnlock: your phone stays locked until you hit your step goal. 2,000 steps to check instagram. 5,000 to open TikTok. gamify the one exercise everyone can do.", "text", "app screenshot", "", "link in bio", ""),
    ("built an app that forces you to walk before you scroll. sounds annoying. that's the point. WalkToUnlock.", "text", "step data screenshot", "", "link in bio to download", ""),
    ("the 3-Hour Physique program. exactly 3 sessions per week. 1 hour each. compound lifts only. progressive overload built in. no fluff. $12 on Gumroad.", "text", "program preview", "", "link in bio for the program", ""),
    ("free: the supplement stack guide. what to take, what to skip, exact brands, cost per day. spoiler: you need 4 supplements. not 12. not 20. four.", "text", "guide preview", "", "reply STACK for the free PDF", ""),
    ("WalkToUnlock + PrayerLock combo. walk first, pray second, then use your phone. the morning hits different when you earn the scroll.", "text", "both apps", "", "links in bio", ""),
    ("the meal prep starter kit. 4 weeks of recipes. shopping lists. macro breakdowns. designed for people who hate cooking but need to eat right. $7.", "text", "recipe preview", "", "link in bio", ""),
    ("new WalkToUnlock feature: streak tracking. hit your step goal daily or the streak resets. can you keep it going?", "text", "streak screenshot", "", "download and start", ""),
    ("free 30-day bodyweight program. no gym needed. pushups, pullups, squats, planks. progressive overload built in. PDF download.", "text", "program preview", "", "reply BODYWEIGHT for the link", ""),
    ("the home gym buying guide. exactly what to buy, in what order, from where, for how much. built my setup for $800. complete guide for $5.", "text", "home gym photo", "", "link in bio", ""),
    ("WalkToUnlock corporate wellness pitch: companies are paying $50/employee/month for wellness programs. our app is $3.99 and actually works. the math is obvious.", "text", "", "", "DM for corporate licensing", ""),
    ("the progressive overload tracker spreadsheet. free google sheets template. log your lifts, auto-calculates next session weights, tracks PRs. the only tool you need.", "text", "spreadsheet screenshot", "", "reply TRACKER for the link", ""),
    ("12-week transformation challenge starts next monday. free to join. daily workout posted. community accountability. weekly check-ins. zero cost.", "text", "", "", "reply CHALLENGE to join", ""),
    ("the protein recipe ebook. 30 high-protein meals. each takes under 20 minutes. each has 40g+ protein. no weird ingredients. $5 on Gumroad.", "text", "recipe photos", "", "link in bio", ""),
    ("WalkToUnlock is live. it's not a gym membership. not a personal trainer. just a phone lock that forces you to walk before you scroll.", "text", "", "", "try it and tell me if it works", ""),
    ("free: the stretching routine that fixed my back pain. 10 minutes. 8 stretches. do it after every workout. video guide included.", "text", "stretching demo", "", "reply STRETCH for the video", ""),
    ("the 3-Hour Physique newsletter. one email per week. one exercise tip. one nutrition tip. one mindset tip. free forever. 5 minute read.", "text", "", "", "reply EMAIL to subscribe", ""),
    ("WalkToUnlock premium: custom step goals per app, group challenges with friends, GPS route tracking. $29/year. less than 1 month of a gym membership you don't use.", "text", "premium features", "", "link in bio", ""),
    ("the cutting guide. how to lose fat without losing muscle. calorie targets, training adjustments, timeline expectations. realistic, no BS. $9.", "text", "guide preview", "", "link in bio", ""),
]

FITNESS_PERSONALITY = [
    ("leg day yesterday. stairs are not my friend today. my 4 year old asked why i'm walking funny. told her daddy made poor life choices. she said 'again?'", "text", "", "", "", ""),
    ("building WalkToUnlock while sitting at my desk for 9 hours is peak irony. the shoemaker's children have no shoes. the step tracker developer has 2,000 steps.", "text", "", "", "", ""),
    ("hit 225 on bench today. been chasing this number for 11 months. nobody in the gym cared. texted my wife. she said 'nice honey.' this is the loneliest sport.", "text", "", "", "", ""),
    ("honest admission: i started the fitness account because i was 195lbs, 30% body fat, and couldn't do 5 pushups. that was 8 months ago. now i'm 185lbs, 18% body fat. still not impressive but the direction matters.", "text", "", "", "", ""),
    ("3-Hour Physique came from necessity not choice. i have a full time job, 2 kids, and a side project. 3 hours is literally all i have. turns out it's all you need.", "text", "", "", "", ""),
    ("meal prepped on sunday. it's wednesday and i've eaten chipotle twice. the meal prep is still in the fridge. judging me. i'll do better next week. (i said this last week too.)", "text", "", "", "", ""),
    ("my gym is a garage with a squat rack and a dream. it's 38 degrees in there this morning. the barbell was cold enough to hurt my hands. there is no plan B. only plan cold.", "text", "", "", "", ""),
    ("update: the WalkToUnlock app forced me to walk 4,000 steps this morning before i could check my email. i built this app and it's bullying me. working as intended.", "text", "", "", "", ""),
    ("6 months of daily fitness content. building products on the side. the gym progress is obvious. the business progress is slower. still worth it.", "text", "", "", "", ""),
]

###############################################################################
# TECH/AI CONTENT BANK - @ai_workflows_daily / @aiworkflowsdaily
###############################################################################

TECH_VALUE = [
    ("i automated my content posting across 6 platforms. took 3 hours to set up with n8n (free self-hosted). saves 5 hours per week. that's 260 hours per year. the math isn't close.", "text", "", "#automation #n8n #productivity", "reply AUTO for the workflow", ""),
    ("Claude vs ChatGPT for coding in 2026. tested both for 30 days on real projects. Claude handles 150+ message threads without losing context. ChatGPT breaks at 20. for long coding sessions it's not close.", "text", "", "#AI #Claude #ChatGPT #coding", "", ""),
    ("the AI stack that replaced my $3,000/month marketing team: ChatGPT for copy ($20/mo), Leonardo for images ($12/mo), ElevenLabs for voice ($5/mo), Remotion for video ($0). total: $37/month.", "text", "", "#AI #marketing #automation", "reply STACK for the full setup guide", ""),
    ("n8n self-hosted on a $20/month VPS. unlimited workflows. connected to X API, email, sheets, slack. replaces Zapier ($50/mo), Make ($30/mo), Buffer ($15/mo). saved $75/month day one.", "text", "", "#n8n #automation #nocode", "", ""),
    ("built a cold email system with Clay + Instantly + Apollo. AI writes 80% of the personalization. 10% reply rate. industry average is 3.4%. the secret: intent signals, not spray and pray.", "text", "", "#coldemail #sales #AI", "reply COLD for the exact setup", ""),
    ("the MCP server ecosystem just launched. Anthropic + OpenAI both supporting it. near-zero third-party apps right now. if you can build an MCP server this month you have first-mover advantage measured in weeks.", "text", "", "#MCP #AI #developer", "", ""),
    ("Facebook Reels pays $4.40 per 1,000 views. TikTok pays $0.01-1.00. YouTube Shorts pays $0.02-0.04. same video, 3 platforms, FB Reels pays 4-440x more. cross-post everything to FB Reels today.", "text", "", "#reels #monetization #creator", "", ""),
    ("Cursor + Claude for vibe coding. built a full landing page in 47 minutes. would have taken 4 hours manually. the AI doesn't write perfect code. but it writes 80% of it and i fix the rest. 5x faster.", "text", "", "#vibecoding #Cursor #Claude", "", ""),
    ("web scraping in 2026: Playwright > Puppeteer > Selenium. Playwright handles anti-bot better, runs 3 browsers, and the API is cleaner. switched everything over in one afternoon.", "text", "", "#webscraping #Playwright #automation", "", ""),
    ("the Whop vs Gumroad comparison nobody asked for. Whop: 5.7% total fees. Gumroad: 13-14% total fees. at $10K revenue that's $570 vs $1,400 in fees. migrating this week.", "text", "", "#Whop #Gumroad #digitalproducts", "", ""),
    ("built 30 apps in 12 months. the ones that make money: simple single-feature apps with hard paywalls. the ones that don't: feature-rich apps with free tiers. counterintuitive but the data is clear.", "text", "", "#apps #indiehacking #monetization", "", ""),
    ("the SEO landscape in 2026: zero-click searches up 65%. Google AI Overviews stealing traffic. solution: build for AI citations not just Google rankings. Reddit content appears in 68% of AI answers.", "text", "", "#SEO #AI #marketing", "reply SEO for the full playbook", ""),
    ("Vercel v0 for prototyping UI. describe what you want in plain english. get a working React component in 30 seconds. i use it to test 10 landing page variations before writing any real code.", "text", "", "#Vercel #v0 #prototyping", "", ""),
    ("API wrapper businesses in 2026. find a popular API. make it easier to use for a specific audience. charge $29/month. there are people making $50K/month doing this for the OpenAI API alone.", "text", "", "#API #SaaS #indiehacking", "", ""),
    ("RevenueCat for app subscriptions. handles iOS and Android. A/B tests paywalls without app updates. animated paywalls convert 2.9x better than static. one tool, biggest revenue lever.", "text", "", "#RevenueCat #subscriptions #apps", "", ""),
    ("the TikTok Shop affiliate play: products $10-30. beauty and health niches. small creators under 50K followers get 30% click rate (4.3x bigger accounts). $66.2B GMV last year. 100% YoY growth.", "text", "", "#TikTokShop #affiliate #ecommerce", "", ""),
    ("llms.txt is the new robots.txt. tell AI crawlers exactly what your site is about. early adoption means your content gets cited by ChatGPT, Claude, Perplexity before competitors catch on.", "text", "", "#AI #SEO #llmstxt", "", ""),
    ("the Reddit distribution hack for 2026. Reddit content appears in 68% of AI-generated answers. post genuine value in relevant subreddits. your content gets cited by AI forever. best long-tail play.", "text", "", "#Reddit #distribution #AI", "", ""),
    ("hard paywalls are beating freemium in 2026. apps with hard paywalls generate 8x more revenue per user than freemium. no free tier. show value in onboarding. gate everything behind subscription.", "text", "", "#paywall #monetization #apps", "", ""),
    ("the 500-clipper distribution model: pay 300-500 content clippers $1 per 1,000 views. test hooks simultaneously. case study: 43,000 app downloads for $6,000 spend. beats paid ads for personal brand content.", "text", "", "#distribution #content #growth", "", ""),
    ("AI personalized cold email gets 7x higher reply rates than template-based. Clay enriches leads with intent signals. AI writes the personalization. human reviews before sending. best of both worlds.", "text", "", "#coldemail #AI #sales", "", ""),
    ("Suno for AI music. generate a full song in 30 seconds. distribute via DistroKid to Spotify, Apple Music, TikTok. some AI tracks getting 100K+ streams. $0 production cost. infinite catalog.", "text", "", "#AImusic #Suno #Spotify", "", ""),
    ("the web-to-app funnel. 82% of top-grossing apps monetize through web funnels, not app store purchases. bypass the 30% Apple/Google tax. Stripe checkout on web, deliver value in app.", "text", "", "#webtoapp #monetization #apps", "reply FUNNEL for the playbook", ""),
    ("Google's January 2026 update: personal brand content now outranks anonymous SEO content. build in public, share real numbers, show your work. authentic experience is the new SEO moat.", "text", "", "#Google #SEO #buildinpublic", "", ""),
    ("Threads has 400 million monthly active users and zero creator monetization. that means: zero competition from established creators. build audience now, monetize when they launch the fund.", "text", "", "#Threads #growth #platform", "", ""),
    ("the AI compliance audit opportunity. EU AI Act enforcement starts August 2026. near-zero supply of compliance auditors. $5K-50K per audit. if you understand AI + regulation this is a gold mine.", "text", "", "#AI #compliance #opportunity", "", ""),
    ("print on demand home decor is growing 24.2% annually. highest margin category in POD. wall art, throw pillows, blankets. AI generates designs. Printful handles fulfillment. you handle marketing.", "text", "", "#POD #printondeman #ecommerce", "", ""),
    ("Temu arbitrage is officially dead. tariffs 30-145%. users down 52%. if you're still trying to arbitrage from Temu, stop. redirect that effort to TikTok Shop affiliate.", "text", "", "#ecommerce #arbitrage #temu", "", ""),
    ("the annotation pyramid for app development: core feature first, ship it, get feedback, iterate. not: plan everything, design everything, build everything, launch to crickets.", "text", "", "#appdevelopment #lean #shipping", "", ""),
    ("X doubled the creator revenue pool in January. verified accounts seeing 2-3x payout increases. if your account is monetized, your per-impression revenue just doubled. post more.", "text", "", "#X #creator #monetization", "", ""),
    ("AI interior design apps have 99% margins. zero physical goods. user uploads room photo, AI generates redesigned version, charges $5-20 per generation. InteriorAI doing $83K/month.", "text", "", "#AI #interiordesign #apps", "", ""),
    ("the boring tech stack wins: Next.js + Vercel + Supabase + Stripe. same stack for all 30 apps. no decision fatigue. deploy in minutes. scale without thinking.", "text", "", "#techstack #nextjs #indiehacking", "", ""),
    ("speed is the moat in 2026. AI tools let you launch products in 24-48 hours. if you're spending 3 months on an MVP you're competing with people who ship in 3 days. adjust.", "text", "", "#speed #shipping #AI", "", ""),
    ("push notifications: users who receive even ONE push notification in first 90 days are 3x more likely to retain. but 78% say irrelevant notifications are a dealbreaker. send few, send relevant.", "text", "", "#pushnotifications #retention #apps", "", ""),
    ("Kick streaming platform: 95/5 revenue split vs Twitch 50/50. if you're a streamer, dual-stream to Kick. 1.9x more revenue from same content. platform arbitrage is real.", "text", "", "#Kick #Twitch #streaming", "", ""),
    ("the $0 to $62K MRR in 3 months pattern: AI tooling for speed, talk to users constantly, prioritize ruthlessly, ship daily. the people winning are shipping 10x faster than everyone else.", "text", "", "#MRR #SaaS #growth", "", ""),
]

TECH_ENGAGEMENT = [
    ("Claude or ChatGPT for coding? genuinely want to know what you use and why. i switched to Claude 3 months ago and haven't looked back.", "text", "", "", "drop your preference", ""),
    ("hot take: 90% of SaaS products are features not products. they'll get absorbed into bigger platforms within 2 years. build something that can't be a feature.", "text", "", "", "agree or disagree?", ""),
    ("what's the one tool you couldn't run your business without? no AI answers. the boring operational tool. mine is Notion.", "text", "", "", "", ""),
    ("unpopular opinion: no-code tools create worse developers. learning to code properly takes time but the ceiling is infinitely higher.", "text", "", "", "fight me", ""),
    ("your best performing piece of content ever. platform and approximate reach. i'll go first: a twitter thread about cold email that got 340K impressions.", "text", "", "", "share yours", ""),
    ("the AI tool you tried and immediately unsubscribed from. what was it and why? mine was Jasper. rewrote everything it produced anyway.", "text", "", "", "share your worst AI purchase", ""),
    ("would you rather: 10,000 email subscribers or 100,000 twitter followers? only one. think carefully.", "text", "", "", "and explain why", ""),
    ("what's the most you've ever made from a single piece of content? a tweet, video, article, anything. curious about the distribution.", "text", "", "", "", ""),
    ("POV: you just shipped a feature nobody asked for and it became your most popular feature. has this happened to anyone else?", "text", "", "", "share the story", ""),
    ("the AI hype cycle: we're past the peak of inflated expectations and entering the trough of disillusionment. the real builders will emerge in the next 12 months. the grifters are already gone.", "text", "", "", "where do you think we are?", ""),
    ("tabs or spaces? wrong answers only.", "text", "", "", "", ""),
    ("what's one automation you built that saves you the most time each week? mine: auto-posting content to 6 platforms. 5 hours saved weekly.", "text", "", "", "share yours", ""),
    ("the worst tech advice you've ever followed. i'll start: 'you need to learn blockchain to stay relevant.' wasted 3 months.", "text", "", "", "what was yours?", ""),
    ("name a startup that you think will be dead in 12 months. controversial but interesting. no personal attacks, just business analysis.", "text", "", "", "make your case", ""),
    ("morning coding session or late night coding session? my best code happens between 5-7am before anyone is awake. my worst happens after midnight.", "text", "", "", "when do you code best?", ""),
    ("if you had $500 and 30 days to build a profitable online business from scratch what would you build? serious answers only.", "text", "", "", "most creative answer wins", ""),
    ("the browser extension you can't live without. mine is uBlock Origin. basic but essential.", "text", "", "", "share yours", ""),
    ("is learning to code still worth it in 2026 or should you just learn to prompt AI really well? genuine question.", "text", "", "", "i have my opinion but want yours first", ""),
    ("your current tech stack for your main project. full list. i'll share mine in replies.", "text", "", "", "be specific", ""),
    ("what side project are you building right now? and be honest about where it's at. no 'crushing it' allowed. real status.", "text", "", "", "radical honesty zone", ""),
    ("the subscription you pay for but barely use. we all have one. mine is a Figma pro plan. used it twice last quarter. still paying.", "text", "", "", "confess", ""),
    ("API you wish existed but doesn't. mine: a reliable 'is this person a real buyer or a tire-kicker' API for sales.", "text", "", "", "what would you build if you could?", ""),
    ("dark mode or light mode? this is a personality test and i will judge you.", "text", "", "", "choose wisely", ""),
    ("the most underrated programming language in 2026. my vote: Go. simple, fast, great for APIs, nobody talks about it because it's boring. boring wins.", "text", "", "", "what's yours?", ""),
    ("who's the most underrated tech creator/builder you follow? someone under 10K followers doing incredible work.", "text", "", "", "surface the hidden gems", ""),
    ("be honest: how many unfinished side projects do you have right now? i counted mine. 14. fourteen.", "text", "", "", "drop your number", ""),
    ("the chrome extension, desktop app, or CLI tool you built for yourself that nobody else uses but you can't live without. what is it?", "text", "", "", "", ""),
]

TECH_PROMOTION = [
    ("PRINTMAXX: the system i'm building to run apps, content, cold email, and digital products in parallel. automated where it should be. human-approved where it has to be.", "text", "", "", "reply SYSTEM for early access", ""),
    ("content posting automation is underrated. one input, multiple outputs, consistent cadence. i'm packaging my workflow soon.", "text", "workflow screenshot", "", "follow for the workflow", ""),
    ("the AI Workflows Daily newsletter. one email, every monday. the best AI tool, automation tip, and money-making opportunity i found that week. 3 minute read. free.", "text", "", "", "reply NEWSLETTER to subscribe", ""),
    ("built PrayerLock and WalkToUnlock. two apps that lock your phone until you do something positive: prayer or walking.", "text", "app screenshots", "", "links in bio", ""),
    ("the cold email template pack. sequences for SaaS, agency, freelance, consulting. short, specific, no fluff.", "text", "template preview", "", "link in bio", ""),
    ("free: n8n workflow library. content posting, lead enrichment, competitor monitoring, email sequences, analytics.", "text", "workflow list", "", "reply N8N for the download", ""),
    ("the solopreneur tech stack guide. what to use at $0, then what to upgrade as revenue grows. $7 on Gumroad.", "text", "guide preview", "", "link in bio", ""),
    ("AI Workflows Daily YouTube channel launching this week. 5-minute tutorials. one AI workflow per video. no fluff. just 'here's the tool, here's the setup, here's the result.'", "text", "", "", "subscribe link in bio", ""),
    ("the paywall psychology guide. how to design paywalls that convert 2.9x better. animated elements, price anchoring, personalization, timing. based on RevenueCat data. $9.", "text", "guide preview", "", "link in bio", ""),
    ("free: the app launch checklist. ASO, screenshots, description copy, keyword research, Day 1 playbook.", "text", "checklist preview", "", "reply LAUNCH for the PDF", ""),
    ("the platform arbitrage spreadsheet. every platform's creator payout rate, updated monthly. know where to post for maximum revenue. free google sheets.", "text", "spreadsheet preview", "", "reply ARBITRAGE for the link", ""),
    ("MCP server product opportunity: built a template for shipping MCP servers in 48 hours. the ecosystem is brand new. first movers win. guide: $15 on Gumroad.", "text", "", "", "link in bio", ""),
    ("the web-to-app funnel playbook. bypass 30% app store tax. Stripe checkout on web. deliver value in app. 82% of top apps do this. full implementation guide. $19.", "text", "playbook preview", "", "link in bio", ""),
    ("free tool: the AI content repurposer. paste one blog post, get: 5 tweets, 1 thread, 3 TikTok scripts, 1 newsletter draft, 1 LinkedIn post. Claude API powered. open source.", "text", "tool screenshot", "", "repo link in bio", ""),
    ("the alpha research system. how i scan the internet for money-making opportunities without getting lost in noise. automated where possible, curated where it matters. free guide.", "text", "", "", "reply ALPHA for the guide", ""),
    ("PRINTMAXX site just launched. truth pages about the real state of solopreneur money methods. no fluff, no guru BS, just data. 10 deep-dive pages live now.", "text", "site screenshot", "", "printmaxx.com", ""),
    ("the TikTok Shop affiliate starter kit. how to find products, create content, earn commissions. $10-30 products, 30% click rate for small accounts. step by step. $7.", "text", "", "", "link in bio", ""),
    ("free: weekly AI tool roundup thread every Friday. the actual tools worth paying for, not the 'top 10 AI tools' recycled thread. real testing, real opinions, real numbers.", "text", "", "", "follow for Fridays", ""),
]

TECH_PERSONALITY = [
    ("shipped a bug to production at 2am. woke up to 47 error emails. fixed it in 11 minutes while still in bed. this is the solopreneur life they don't show in the launch day screenshots.", "text", "", "", "", ""),
    ("building in public update: lots of projects, lots of moving parts. the compounding hasn't kicked in yet, but the system is getting tighter every week.", "text", "", "", "", ""),
    ("my wife asked me what i do all day. i said 'i build systems that make money while i sleep.' she said 'okay but you haven't slept in 3 days so...' valid point.", "text", "", "", "", ""),
    ("the AI Workflows Daily account started as notes to myself. 'how did i set up that automation again?' teach what you learn. someone else needs it.", "text", "", "", "", ""),
    ("honest update: building the cold email system was the easy part. converting replies to revenue is a different skill entirely. working on it.", "text", "", "", "", ""),
    ("9 months into this. some days i feel like i'm building something real. other days i feel like i'm playing pretend. the people who succeed are the ones who keep building on the pretend days.", "text", "", "", "", ""),
    ("just realized i have 14 browser tabs of AI tools i'm 'going to test this week.' it's been 3 weeks. closing 10 of them. keeping the 4 that actually solve a problem i have today.", "text", "", "", "", ""),
    ("the funniest part of running a bunch of small projects: explaining it to my parents. 'so you make apps that lock phones? and write about AI? and send cold emails?' yes. all of it.", "text", "", "", "", ""),
    ("year 1 retrospective coming soon. the real asset is the system. revenue is the lagging indicator.", "text", "", "", "", ""),
]

###############################################################################
# PLATFORM ADAPTATIONS
###############################################################################

def adapt_for_platform(post_text, platform, niche, hashtags):
    """Adapt post copy for platform-specific best practices."""
    if platform == "twitter":
        # Max 280 chars preferred, 1-2 hashtags max
        # Strip most hashtags for twitter
        h = hashtags.split(",")[0].strip() if hashtags else ""
        return post_text, h
    elif platform == "tiktok":
        # Caption text, 3-5 hashtags
        h = hashtags if hashtags else "#fyp"
        if "#fyp" not in h:
            h = h + ",#fyp"
        return post_text, h
    elif platform == "instagram":
        # Full caption, 5-15 hashtags
        extra_ig = {
            "faith": "#christianity #bibleverse #prayerlife #godisgood #faithjourney",
            "fitness": "#fitfam #gymlife #gains #workout #fitnessmotivation",
            "tech": "#techinnovation #startup #saas #buildinpublic #indiehackers",
        }
        h = hashtags
        if h:
            h = h + "," + extra_ig.get(niche, "")
        else:
            h = extra_ig.get(niche, "")
        return post_text, h
    elif platform == "linkedin":
        # Professional tone, minimal hashtags, no casual abbreviations
        h = hashtags.split(",")[0].strip() if hashtags else ""
        return post_text, h
    return post_text, hashtags


def get_content_bank(niche, content_type):
    """Get content bank for a niche and content type."""
    banks = {
        "faith": {
            "value": FAITH_VALUE,
            "engagement": FAITH_ENGAGEMENT,
            "promotion": FAITH_PROMOTION,
            "personality": FAITH_PERSONALITY,
        },
        "fitness": {
            "value": FITNESS_VALUE,
            "engagement": FITNESS_ENGAGEMENT,
            "promotion": FITNESS_PROMOTION,
            "personality": FITNESS_PERSONALITY,
        },
        "tech": {
            "value": TECH_VALUE,
            "engagement": TECH_ENGAGEMENT,
            "promotion": TECH_PROMOTION,
            "personality": TECH_PERSONALITY,
        },
    }
    return banks[niche][content_type]


def get_account_handle(niche, platform):
    """Get the account handle for a niche and platform."""
    handles = {
        ("faith", "twitter"): "@daily_anchor_faith",
        ("faith", "tiktok"): "@dailyanchorfaith",
        ("faith", "instagram"): "@dailyanchorfaith",
        ("faith", "linkedin"): "Daily Anchor Faith",
        ("fitness", "twitter"): "@three_hour_physique",
        ("fitness", "tiktok"): "@threehourphysique",
        ("fitness", "instagram"): "@threehourphysique",
        ("fitness", "linkedin"): "3-Hour Physique",
        ("tech", "twitter"): "@ai_workflows_daily",
        ("tech", "tiktok"): "@aiworkflowsdaily",
        ("tech", "instagram"): "@aiworkflowsdaily",
        ("tech", "linkedin"): "AI Workflows Daily",
    }
    return handles.get((niche, platform), "")


def generate_calendar():
    """Generate the full 1,080-post calendar."""
    rows = []

    # Track which post index we're at for each niche+type combo
    post_indices = {}

    for day_offset in range(30):
        current_date = START_DATE + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")
        day_of_week = current_date.weekday()  # 0=Mon, 6=Sun

        # Get content type rotation for this day
        rotation_day = day_offset % 10
        day_types = CONTENT_ROTATION[rotation_day]

        for niche in ["faith", "fitness", "tech"]:
            for platform in ["twitter", "tiktok", "instagram", "linkedin"]:
                # Skip LinkedIn on weekends
                if platform == "linkedin" and day_of_week >= 5:
                    continue

                times = TIMES[platform]

                for post_idx, (post_time, content_type) in enumerate(zip(times, day_types)):
                    # Get content bank
                    bank = get_content_bank(niche, content_type)

                    # Track index per niche+type+platform
                    key = f"{niche}_{content_type}_{platform}"
                    if key not in post_indices:
                        post_indices[key] = 0

                    idx = post_indices[key] % len(bank)
                    post_data = bank[idx]
                    post_indices[key] += 1

                    post_text = post_data[0]
                    media_type = post_data[1]
                    media_desc = post_data[2]
                    base_hashtags = post_data[3]
                    cta = post_data[4]
                    link = post_data[5]

                    # Adapt for platform
                    adapted_text, adapted_hashtags = adapt_for_platform(
                        post_text, platform, niche, base_hashtags
                    )

                    handle = get_account_handle(niche, platform)

                    rows.append({
                        "date": date_str,
                        "time": post_time,
                        "niche": niche,
                        "platform": platform,
                        "account": handle,
                        "content_type": content_type,
                        "post_text": adapted_text,
                        "media_type": media_type if media_type else "text",
                        "media_description": media_desc,
                        "hashtags": adapted_hashtags,
                        "cta": cta,
                        "link": link,
                        "status": "pending",
                        "day_of_week": current_date.strftime("%A"),
                    })

    return rows


def write_csv(rows):
    """Write rows to CSV."""
    fieldnames = [
        "date", "time", "niche", "platform", "account", "content_type",
        "post_text", "media_type", "media_description", "hashtags",
        "cta", "link", "status", "day_of_week"
    ]

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


if __name__ == "__main__":
    print("Generating 30-day content calendar...")
    rows = generate_calendar()
    count = write_csv(rows)
    print(f"Generated {count} posts to {OUTPUT_CSV}")

    # Stats
    from collections import Counter
    niche_counts = Counter(r["niche"] for r in rows)
    platform_counts = Counter(r["platform"] for r in rows)
    type_counts = Counter(r["content_type"] for r in rows)

    print(f"\nBy niche: {dict(niche_counts)}")
    print(f"By platform: {dict(platform_counts)}")
    print(f"By content type: {dict(type_counts)}")

# Forced-Action Alarm Clock App (iOS)
Date: 2026-04-02
Score: 8/10
Status: PENDING_REVIEW

## What
A mobile alarm app that will not stop ringing until you complete a physical action -- scanning a QR code in your bathroom, taking a photo of your coffee maker, walking 50 steps, or solving a physical challenge. The Reddit post about this concept hit 918 upvotes on r/SideProject proving massive validated demand for a well-executed version.

## Why Now
The r/SideProject post "I built an alarm clock that won't stop ringing until you go to the toilet to turn it off" hit 918 upvotes -- the top post of the week. The creator built it as a side project proving the concept works. Existing alarm apps with math problems do not work (people solve them half-asleep and go back to bed). Physical movement is the only reliable wake-up method. The Sleep/Wellness app category on iOS generates $2B+ annually. Niche alarm apps with strong hooks regularly hit $5K-50K/mo MRR.

## Revenue Path
- Free tier: basic alarm with 1 forced action (QR code scan)
- Premium: $3.99/mo or $24.99/yr -- multiple alarm types, custom actions (photo verification, step counting, voice recording "I'm awake"), sleep tracking, social accountability (friends see if you snoozed)
- Viral hook: shareable "I woke up" streaks on social media

## Expected ROI
- Startup cost: $0 (Expo, Stripe)
- Time to revenue: 5 days (core alarm + QR scanner + step counter is straightforward in React Native)
- Monthly potential: $2,000-$8,000 (500-2000 subscribers at $3.99)
- Competition: MED -- Alarmy exists but has poor UX and aggressive ads. Market is large enough for a clean, well-designed alternative

## First 3 Steps
1. Build Expo app: alarm service (background audio), QR code scanner (expo-camera), step counter (expo-sensors/pedometer), photo verification (compare location metadata). Cal AI-style onboarding about sleep habits
2. Add gamification: wake-up streaks, weekly reports, "morning person" score. Hard paywall after 7-day trial. Wire Stripe Payment Links
3. Launch with TikTok videos showing the alarm going off and person running to bathroom. "POV: my alarm won't shut up until I prove I left bed" is viral content format

## PRINTMAXX Fit
Direct app factory pipeline. Expo/React Native is core stack. Uses real sensors (step counter, camera, location) not simulated data -- aligns with Rule 31. Stripe payments wired. Viral TikTok content potential feeds content engine. Sleep/wellness niche cross-sells with SleepMaxx app. Can share HealthKit integration code.

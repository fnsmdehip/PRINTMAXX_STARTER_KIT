# In-app review prompt copy

Rating prompts, feedback collection, and review routing.

---

## Two-step rating flow

Step 1 routes happy users to app store, unhappy users to feedback form.

### Step 1: Satisfaction check

**Prompt A (Simple):**
```
How's [App Name] working for you?

[Great] [Could be better]
```

**Prompt B (Emoji scale):**
```
How would you rate your experience so far?

[😞] [😐] [🙂] [😄]
```

**Prompt C (Specific):**
```
Has [App Name] helped you [core benefit]?

[Yes, it has] [Not yet]
```

---

### Step 2a: Happy path (Great / 🙂😄 / Yes)

```
Glad to hear it!

Would you mind sharing that on the App Store? It helps other people find the app.

[Leave a Review] [Not Now]
```

---

### Step 2b: Unhappy path (Could be better / 😞😐 / Not yet)

```
Thanks for the honesty.

What could make [App Name] better for you?

[Text input field]

[Send Feedback] [Cancel]
```

Follow-up after feedback submitted:
```
Got it. I read every piece of feedback and use it to improve the app.

Thanks for taking the time.

[Close]
```

---

## Trigger conditions

**When to show prompt:**

Good timing:
- After completing a core task successfully
- After reaching a milestone (first week, 10th use, etc.)
- After a feature they requested ships
- When they return after 7+ day absence

Bad timing:
- During onboarding
- After an error or crash
- During a complex multi-step flow
- When they just opened the app
- If they dismissed a prompt in last 30 days

**Frequency limits:**
- Max 1 prompt per 30 days
- Max 3 total prompts ever (then stop asking)
- Reset if major version update ships

---

## iOS vs Android implementation

### iOS (SKStoreReviewController)

```swift
// iOS limits you to 3 prompts per year
// System decides whether to actually show it
// You can only request, not guarantee display

import StoreKit

func requestReview() {
    if let scene = UIApplication.shared.connectedScenes.first(where: { $0.activationState == .foregroundActive }) as? UIWindowScene {
        SKStoreReviewController.requestReview(in: scene)
    }
}
```

**iOS rules:**
- Use SKStoreReviewController only
- Don't show custom prompt before system prompt
- Don't explain what's about to happen
- Apple may not show the prompt (they decide)

### Android (In-App Review API)

```kotlin
// Android allows more control but still has limits
val manager = ReviewManagerFactory.create(context)
val request = manager.requestReviewFlow()
request.addOnCompleteListener { task ->
    if (task.isSuccessful) {
        val reviewInfo = task.result
        manager.launchReviewFlow(activity, reviewInfo)
    }
}
```

**Android rules:**
- Use Play Core library's in-app review API
- Don't ask immediately after install
- Don't interrupt user flow
- Can't know if user actually left review

---

## Alternative: Direct to store

If you want more control (not using native prompt):

```
Enjoying [App Name]?

[Yes, love it!] [It's okay] [Not really]
```

**"Yes, love it!" response:**
```
Awesome! Would you share that on the [App Store / Play Store]?

A review helps other people find the app.

[Go to Store] [Maybe Later]
```

Then open: `https://apps.apple.com/app/id[YOUR_APP_ID]?action=write-review`

---

## Copy variations by app type

### Productivity app
```
You just finished [task]. Nice work.

Quick question: Is [App Name] saving you time?

[Yes] [Not yet]
```

### Health/fitness app
```
You've logged [X] days in a row.

Is [App Name] helping you stay on track?

[Yes, it helps] [Could be better]
```

### Utility app
```
You've used [feature] [X] times.

Is it working well for you?

[Works great] [Having issues]
```

---

## Never do this

- Don't ask "Rate us 5 stars"
- Don't offer rewards for reviews
- Don't show prompt after negative experience
- Don't block features until they rate
- Don't show prompt on first launch
- Don't ask more than once per month
- Don't guilt trip ("We're a small team...")

---

## Tracking

Log these events:
- `review_prompt_shown`
- `review_prompt_positive_response`
- `review_prompt_negative_response`
- `review_prompt_dismissed`
- `feedback_submitted`
- `app_store_opened`

Use this data to optimize timing and copy.

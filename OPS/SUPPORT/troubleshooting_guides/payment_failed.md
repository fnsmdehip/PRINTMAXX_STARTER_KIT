# Troubleshooting: Payment failed

**Symptoms:** Credit card declined, subscription not activating after payment attempt, "payment failed" error messages, PayPal errors.

---

## Quick diagnosis

Ask the customer:
1. What error message did you see? (Exact text helps)
2. What payment method? (Card type, PayPal, Apple Pay, etc.)
3. Is this a new subscription or renewal?
4. Have you used this card successfully before?

---

## Common decline reasons

### Card issues (most common)

**Insufficient funds**
- Customer needs to use different card or add funds
- We can't see their balance. Be tactful.

**Card expired**
- Check expiration date in Stripe/billing system
- Customer needs to update payment method

**Incorrect card details**
- Wrong number, CVV, or billing zip
- Have customer re-enter carefully

**Card blocked by bank**
- International transactions sometimes flagged
- Customer should call their bank to approve
- Or try different card

**Prepaid cards**
- Some prepaid/gift cards don't work for subscriptions
- Need card that allows recurring payments

**Lost/stolen card**
- Card was reported and cancelled
- Customer needs new card

### Address verification failure

AVS (Address Verification Service) failed:
- Billing address doesn't match bank's records
- Common with new addresses or apartments
- Have customer verify address matches bank statement exactly

### 3D Secure / SCA issues

European cards require extra verification:
- Customer should complete bank verification popup
- If popup doesn't appear: try different browser
- If popup fails: contact bank

---

## Platform-specific issues

### Stripe payments (website)

**"Your card was declined"**
1. Check Stripe Dashboard > Payments > Failed
2. Look at decline code:
   - `insufficient_funds` - Customer issue
   - `card_declined` - Bank issue
   - `expired_card` - Card expired
   - `incorrect_cvc` - Wrong CVV entered
   - `processing_error` - Our issue, retry

**"Payment method not supported"**
- Some card types not enabled
- Customer should try different card
- Or we need to enable that card type in Stripe

### iOS App Store

**"Your payment method was declined"**
- Apple manages these payments
- We can't see why it failed
- Customer should:
  1. Go to App Store > Account > Manage Payments
  2. Update or add new payment method
  3. Retry purchase

**"Cannot connect to App Store"**
- Network issue
- Try on wifi
- Sign out/in to Apple ID

### Google Play

**"Transaction cannot be completed"**
- Customer should:
  1. Go to Play Store > Account > Payment methods
  2. Update payment info
  3. Retry

**"Authentication required"**
- Google needs password re-entry
- Have customer sign out/in to Google account

### PayPal

**"Something went wrong"**
1. Customer should check PayPal has valid funding source
2. PayPal balance or linked card
3. Try linking different card to PayPal
4. If PayPal account limited, they need to resolve with PayPal

---

## Retry guidance

**When to retry:**
- After customer updates payment method
- After customer contacts bank
- After 24 hours (some temporary blocks lift)

**When NOT to retry:**
- Rapid retries can trigger fraud alerts
- If declined 3+ times, stop and troubleshoot
- If customer says bank confirmed no issue, try different card

---

## Manual payment alternatives

If card keeps failing and customer is frustrated:

1. **Different card** - Most effective
2. **PayPal** - If we support it
3. **Apple Pay / Google Pay** - Different auth flow, sometimes works
4. **Invoice** - For enterprise/annual plans, we can send invoice for bank transfer

---

## Helping frustrated customers

Payment issues are stressful. Tips:

**Don't:**
- Imply they have no money
- Blame their bank aggressively
- Make them feel stupid

**Do:**
- Acknowledge it's frustrating
- Give concrete next steps
- Offer alternative payment methods
- Extend trial if they're trying to convert

Example:
> "Payment issues are annoying. Most common cause is your bank flagging the transaction as suspicious. Try giving them a quick call to approve it, or use a different card. I've extended your trial 3 days while you sort it out."

---

## Check for fraud indicators

Before helping with payment issues, check:
- Is email clearly fake? (random123@tempmail.com)
- Multiple failed attempts with different cards?
- Account created minutes ago?
- Location mismatch between IP and billing?

If suspicious, escalate before helping. We don't help fraudsters troubleshoot.

---

## Escalation criteria

Escalate to engineering when:
- Stripe shows successful charge but subscription didn't activate
- Same card worked before, now failing with `processing_error`
- Multiple customers report failures simultaneously
- Webhook failures in logs

Escalate to finance when:
- Enterprise customer needs invoice
- Refund requested but payment in weird state
- Currency or regional pricing questions

Include:
- Customer email
- Payment ID or transaction ID
- Error code/message
- Steps tried

---

## Quick reference

| Error | Likely cause | Tell customer |
|-------|--------------|---------------|
| Card declined | Many possible | Try different card or call bank |
| Insufficient funds | No money | Use different card (be tactful) |
| Expired card | Card expired | Update card in payment settings |
| Incorrect CVC | Wrong CVV | Re-enter card details |
| AVS failure | Address mismatch | Use address on bank statement |
| Processing error | Our system | Wait 10 min, retry |
| 3D Secure failed | Bank verification | Complete verification popup |

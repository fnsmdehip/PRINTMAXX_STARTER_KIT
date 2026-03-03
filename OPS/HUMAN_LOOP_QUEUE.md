# Human Loop Queue

Generated: 2026-03-02 20:31:22

Node role: `worker`

Critical actions are blocked until explicitly approved.

## Pending Approvals

- [ ] `ACCOUNT_GUMROAD` - Activate Gumroad account
- [ ] `ACCOUNT_EBAY` - Activate eBay account
- [ ] `ACCOUNT_ETSY` - Activate Etsy account
- [ ] `ACCOUNT_REDBUBBLE` - Activate Redbubble account
- [ ] `ACCOUNT_AMAZON` - Activate Amazon account
- [ ] `EMAIL_INFRA` - Configure Gmail/Resend + PHYSICAL_ADDRESS in SECRETS/PAYMENT_INFO.md (required for LIVE_EMAIL_SEND).
- [ ] `GUMROAD_API_TOKEN` - Add GUMROAD_ACCESS_TOKEN to SECRETS/PAYMENT_INFO.md for AUTO_LIST_ECOM.
- [ ] `LIVE_EMAIL_SEND` - Approve live cold-email send (100 max)
- [ ] `COMPLIANCE_HIGH_RISK` - High compliance risk: 6 CRITICAL issues in LEDGER/compliance_scan_2026_03_02.json. Required for live high-upside execution.

## Approved (Persistent)

- [x] `AUTO_LIST_ECOM`

## Resume Command

Run Ship Captain again after approvals are done.


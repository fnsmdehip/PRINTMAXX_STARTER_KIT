#!/usr/bin/env python3
"""Create Stripe Payment Links for all 4 iOS apps."""
import os
import json
import stripe
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
if not stripe.api_key:
    print("ERROR: STRIPE_SECRET_KEY not found in .env")
    exit(1)

APPS = {
    "nutrisnap": {
        "annual_price": "price_1TEh4rKlbvFndmYLFg2VB9Ty",
        "monthly_price": "price_1TEh4rKlbvFndmYL8aUlFGBp",
        "name": "NutriSnap",
    },
    "scripture-streak": {
        "annual_price": "price_1TEh4tKlbvFndmYL8sNnKuHl",
        "monthly_price": "price_1TDV5vKlbvFndmYLUasaEC2s",
        "name": "Scripture Streak",
    },
    "pocket-alexandria": {
        "annual_price": "price_1TEh4sKlbvFndmYL7NAfIFxw",
        "monthly_price": "price_1TEh4sKlbvFndmYLcAMldUQT",
        "name": "Pocket Alexandria",
    },
    "consentvault": {
        "annual_price": "price_1TEh4tKlbvFndmYLSNBrwPMw",
        "monthly_price": "price_1TEh4tKlbvFndmYLaNxft7FB",
        "name": "ConsentVault",
    },
}

SUCCESS_URL = "https://printmaxx-payments.surge.sh/success?app={app}&plan={plan}"

results = {}

for app_id, config in APPS.items():
    results[app_id] = {}
    for plan in ["annual", "monthly"]:
        price_id = config[f"{plan}_price"]
        try:
            link = stripe.PaymentLink.create(
                line_items=[{"price": price_id, "quantity": 1}],
                after_completion={
                    "type": "redirect",
                    "redirect": {"url": SUCCESS_URL.format(app=app_id, plan=plan)},
                },
                allow_promotion_codes=True,
                metadata={"app": app_id, "plan": plan},
            )
            results[app_id][plan] = link.url
            print(f"  {config['name']} {plan}: {link.url}")
        except stripe.error.StripeError as e:
            print(f"  ERROR {config['name']} {plan}: {e}")
            results[app_id][plan] = f"ERROR: {e}"

# Save results
output_path = PROJECT_ROOT / "MONEY_METHODS" / "APP_FACTORY" / "stripe_payment_links.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\nSaved to {output_path}")
print(json.dumps(results, indent=2))

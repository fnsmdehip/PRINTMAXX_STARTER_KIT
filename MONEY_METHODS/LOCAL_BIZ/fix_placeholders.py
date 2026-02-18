#!/usr/bin/env python3
"""Replace ALL {{VARIABLE}} and {{VARIABLE:default}} placeholders in demo site HTML files."""
import re
import os

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/templates"

# --- DENTAL ---
dental_vars = {
    "BUSINESS_NAME": "Bright Smile Family Dental",
    "PHONE": "(512) 555-0142",
    "ADDRESS": "2847 Lakewood Dr, Austin, TX 78704",
    "RATING_STARS": "4.9",
    "REVIEW_COUNT": "200",
    "EMAIL": "info@brightsmileaustin.com",
    "IMAGE_PLACEHOLDER": "Office / Team Photo",
}

# --- RESTAURANT ---
restaurant_vars = {
    "BUSINESS_NAME": "The Oak Table",
    "PHONE": "(512) 555-0198",
    "ADDRESS": "415 Congress Ave, Austin, TX 78701",
    "CUISINE_TYPE": "Italian",
    "EMAIL": "hello@theoaktable.com",
}

# --- FITNESS ---
fitness_vars = {
    "BUSINESS_NAME": "Iron Republic Fitness",
    "PHONE": "(512) 555-0267",
    "ADDRESS": "1923 S Lamar Blvd, Austin, TX 78704",
    "EMAIL": "info@ironrepublicfitness.com",
}

# --- LEGAL ---
legal_vars = {
    "BUSINESS_NAME": "Chen & Associates",
    "PHONE": "(512) 555-0315",
    "ADDRESS": "600 Congress Ave Ste 1400, Austin, TX 78701",
    "PRACTICE_AREA": "Personal Injury",
    "LEAD_ATTORNEY": "David Chen, Esq.",
    "LEAD_ATTORNEY_TITLE": "Founding Partner | Board Certified Trial Lawyer",
    "EMAIL": "consult@chenlaw.com",
    "IMAGE_PLACEHOLDER": "Attorney / Office Photo",
}

# --- PLUMBER ---
plumber_vars = {
    "BUSINESS_NAME": "Reliable Flow Plumbing",
    "PHONE": "(512) 555-0389",
    "ADDRESS": "4710 E Riverside Dr",
    "CITY": "Austin",
    "STATE": "TX",
    "ZIP": "78741",
    "LICENSE_NUMBER": "M-42891",
    "YEARS_IN_BUSINESS": "18",
    "JOBS_COMPLETED": "12,000",
    "RATING_STARS": "4.8",
    "REVIEW_COUNT": "340",
    "EMAIL": "service@reliableflowatx.com",
    "SERVICE_AREA_1": "Round Rock",
    "SERVICE_AREA_2": "Cedar Park",
    "SERVICE_AREA_3": "Pflugerville",
    "SERVICE_AREA_4": "Lakeway",
    "SERVICE_AREA_5": "Bee Cave",
    "MAP_LNG": "-97.7431",
    "MAP_LAT": "30.2672",
}

# --- REALTOR ---
realtor_vars = {
    "BUSINESS_NAME": "Sarah Martinez Real Estate",
    "PHONE": "(512) 555-0456",
    "ADDRESS": "1250 S Capital of Texas Hwy",
    "CITY": "Austin",
    "STATE": "TX",
    "ZIP": "78746",
    "REVIEW_COUNT": "127",
    "TOTAL_SOLD": "284",
    "VOLUME_SOLD": "142",
    "DAYS_ON_MARKET": "14",
    "AVG_SALE_PRICE": "485,000",
    "SALE_TO_LIST": "101.3",
    "AGENT_FIRST_NAME": "Sarah",
    "YEARS_EXPERIENCE": "12",
    "BROKERAGE_NAME": "Keller Williams Realty",
    "LICENSE_NUMBER": "0648291",
    "SPECIALTIES": "Luxury, Relocation, First-Time Buyers",
    "EMAIL": "sarah@sarahmartinezrealty.com",
    "LISTING_1_PRICE": "549,000",
    "LISTING_1_ADDRESS": "3412 Windsor Rd",
    "LISTING_1_BEDS": "4",
    "LISTING_1_BATHS": "3",
    "LISTING_1_SQFT": "2,450",
    "LISTING_2_PRICE": "389,000",
    "LISTING_2_ADDRESS": "7801 Shoal Creek Blvd #204",
    "LISTING_2_BEDS": "2",
    "LISTING_2_BATHS": "2",
    "LISTING_2_SQFT": "1,380",
    "LISTING_3_PRICE": "725,000",
    "LISTING_3_ADDRESS": "1105 Barton Hills Dr",
    "LISTING_3_BEDS": "5",
    "LISTING_3_BATHS": "4",
    "LISTING_3_SQFT": "3,200",
    "NEIGHBORHOOD_1": "Tarrytown",
    "NEIGHBORHOOD_2": "Barton Hills",
    "NEIGHBORHOOD_3": "South Congress",
    "NEIGHBORHOOD_4": "Mueller",
    "NEIGHBORHOOD_5": "East Austin",
    "NEIGHBORHOOD_6": "Westlake Hills",
    "MAP_LNG": "-97.7431",
    "MAP_LAT": "30.2672",
}

FILES = {
    "dental.html": dental_vars,
    "restaurant.html": restaurant_vars,
    "fitness.html": fitness_vars,
    "legal.html": legal_vars,
    "plumber.html": plumber_vars,
    "realtor.html": realtor_vars,
}


def replace_placeholders(html: str, specific_vars: dict) -> str:
    """Replace all {{VAR}} and {{VAR:default}} patterns.

    Strategy:
    1. If VAR is in specific_vars, use that value (regardless of whether there's a default).
    2. If VAR has a default ({{VAR:default}}), use the default value.
    3. If neither, leave as-is (shouldn't happen if we did our job right).
    """
    def replacer(match):
        full = match.group(0)
        inner = match.group(1)

        # Split on first colon to separate var name from default
        if ":" in inner:
            var_name = inner.split(":", 1)[0]
            default_val = inner.split(":", 1)[1]
        else:
            var_name = inner
            default_val = None

        # Check specific vars first
        if var_name in specific_vars:
            return specific_vars[var_name]

        # Fall back to default
        if default_val is not None:
            return default_val

        # No specific value and no default - flag it
        print(f"  WARNING: No value for {{{{{var_name}}}}} (no default)")
        return full

    return re.sub(r'\{\{([^}]+)\}\}', replacer, html)


def main():
    total_replacements = 0

    for filename, vars_dict in FILES.items():
        filepath = os.path.join(TEMPLATE_DIR, filename)
        print(f"\nProcessing {filename}...")

        with open(filepath, 'r') as f:
            original = f.read()

        # Count placeholders before
        before_count = len(re.findall(r'\{\{[^}]+\}\}', original))

        # Do replacements
        result = replace_placeholders(original, vars_dict)

        # Count remaining
        after_count = len(re.findall(r'\{\{[^}]+\}\}', result))
        replaced = before_count - after_count

        print(f"  Before: {before_count} placeholders")
        print(f"  Replaced: {replaced}")
        print(f"  Remaining: {after_count}")

        if after_count > 0:
            remaining = re.findall(r'\{\{([^}]+)\}\}', result)
            for r in remaining:
                print(f"  STILL PRESENT: {{{{{r}}}}}")

        total_replacements += replaced

        with open(filepath, 'w') as f:
            f.write(result)

        print(f"  SAVED: {filepath}")

    print(f"\n=== DONE: {total_replacements} total replacements across {len(FILES)} files ===")


if __name__ == "__main__":
    main()

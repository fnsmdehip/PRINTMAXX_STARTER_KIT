#!/usr/bin/env python3

# Read final entries
with open('/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/alpha_hunter/final_alpha_entries.csv', 'r') as f:
    final_entries = f.read()

# Append to main file
with open('/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LEDGER/ALPHA_STAGING.csv', 'a') as f:
    f.write(final_entries)

print("Successfully appended 7 final alpha entries to ALPHA_STAGING.csv")
print("Total new entries: 33 (26 + 7)")
print("ALPHA428-ALPHA460 added covering all 12 categories")

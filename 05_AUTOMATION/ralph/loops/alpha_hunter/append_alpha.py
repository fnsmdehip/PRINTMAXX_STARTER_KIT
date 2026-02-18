#!/usr/bin/env python3

# Read new entries
with open('/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/ralph/loops/alpha_hunter/new_alpha_entries.csv', 'r') as f:
    new_entries = f.read()

# Append to main file
with open('/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LEDGER/ALPHA_STAGING.csv', 'a') as f:
    f.write(new_entries)

print("Successfully appended 26 new alpha entries to ALPHA_STAGING.csv")

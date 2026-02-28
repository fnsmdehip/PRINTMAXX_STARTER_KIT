# Spreadsheet Compatibility Report

**Date:** 2026-02-27 | **Status:** COMPATIBLE, minor notes

## Verdict: Keep .xlsx (openpyxl) -- no changes needed

Apple Numbers opens .xlsx files natively. Tested PRINTMAXX_MASTER_OPS_ENHANCED_2026-02-27.xlsx (336KB, 19 sheets, 5,200+ rows) -- opens fine in Numbers.

## What our builder scripts use (openpyxl features)

| Feature | Used? | Numbers Support |
|---------|-------|-----------------|
| Multiple sheets | YES (up to 19) | Full support |
| Font colors + fills | YES (dark theme, cyan/green/red) | Full support |
| Merged cells | YES (~55 instances across scripts) | Full support |
| Column widths | YES | Full support |
| Freeze panes | YES (A2 header freeze) | Full support |
| Borders | YES (thin, colored) | Full support |
| Auto-filter | YES (1 instance in build_infra_stacks.py) | Full support |
| Tab colors | YES (sheet_properties.tabColor) | Partial (Numbers ignores tab colors) |
| Conditional formatting | NO | N/A |
| Charts | NO | N/A |
| Data validation (dropdowns) | NO | N/A |
| Formulas | NO (all values are hardcoded by Python) | N/A |
| Hyperlinks | NO | N/A |

## Known Numbers quirks with .xlsx

1. **Tab colors ignored** -- Numbers does not display sheet tab colors. Cosmetic only, no impact.
2. **Dark theme colors render correctly** -- tested, all fills and fonts display properly.
3. **Merged cells work** -- all 55+ merge_cells calls render correctly in Numbers.
4. **Numbers converts on save** -- if user saves as .numbers, re-opening with openpyxl will fail. Must "Export to Excel" to keep .xlsx format. This is a user workflow note, not a bug.

## Recommendation

**Keep .xlsx with openpyxl. No changes needed.** Reasons:

- openpyxl 3.1.5 is installed and mature
- All 11 builder scripts work correctly
- Numbers opens all files without errors
- No advanced features (charts, formulas, conditional formatting) that could break
- CSV is already used for all LEDGER/ data (the actual source of truth)
- .xlsx serves as formatted presentation layer only -- all real data lives in CSVs
- Switching to .numbers would break all Python automation with zero benefit
- Google Sheets API would add unnecessary account dependency

## One action item

Add a note to builder scripts output: "To edit in Numbers, use File > Export to > Excel when saving to preserve .xlsx format for automation compatibility."

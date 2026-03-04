# PRINTMAXX Compliance Scan Report
**Date:** 2026-03-02 22:34
**Total Issues:** 1699

## Summary
| Severity | Count |
|----------|-------|
| CRITICAL | 7 |
| WARNING | 1687 |
| INFO | 5 |

| Category | Count |
|----------|-------|
| INCOME | 1451 |
| CANSPAM | 211 |
| PII | 30 |
| PLATFORM | 5 |
| HEALTH | 1 |
| FAKE_PROOF | 1 |

## CRITICAL Issues (fix before publishing)

### 1. HEALTH — CONTENT/social/quote_tweets/quotes_drifthour_20260302_210635.csv:11
**Rule:** Health claim that may require substantiation
**Text:** `@drifthour,"curate your inputs. maybe oral hyaluronate reduces inflammation, improves the gut barrier, and prevents cancer, too - like the molecule d.`
**Fix:** Add medical disclaimer or remove unsubstantiated health claim

### 2. CANSPAM — EMAIL/triggering_events/glassdoor_spike_template.txt:0
**Rule:** Email missing unsubscribe mechanism
**Fix:** Add unsubscribe link/instructions to all marketing emails

### 3. CANSPAM — EMAIL/triggering_events/office_move_template.txt:0
**Rule:** Email missing unsubscribe mechanism
**Fix:** Add unsubscribe link/instructions to all marketing emails

### 4. CANSPAM — EMAIL/triggering_events/job_removed_template.txt:0
**Rule:** Email missing unsubscribe mechanism
**Fix:** Add unsubscribe link/instructions to all marketing emails

### 5. CANSPAM — EMAIL/triggering_events/leadership_change_template.txt:0
**Rule:** Email missing unsubscribe mechanism
**Fix:** Add unsubscribe link/instructions to all marketing emails

### 6. CANSPAM — EMAIL/triggering_events/competitor_layoff_template.txt:0
**Rule:** Email missing unsubscribe mechanism
**Fix:** Add unsubscribe link/instructions to all marketing emails

### 7. CANSPAM — EMAIL/triggering_events/sec_filing_change_template.txt:0
**Rule:** Email missing unsubscribe mechanism
**Fix:** Add unsubscribe link/instructions to all marketing emails

## WARNING Issues (review before publishing)

1. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
2. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
3. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
4. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
5. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
6. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
7. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
8. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
9. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
10. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
11. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
12. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
13. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
14. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
15. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
16. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
17. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
18. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
19. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
20. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
21. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
22. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
23. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
24. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
25. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
26. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
27. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
28. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
29. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
30. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
31. **INCOME** `CONTENT/social/auto_generated/alpha_content_2026_02_28.md:45` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
32. **INCOME** `CONTENT/social/auto_generated/alpha_content_2026_02_28.md:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
33. **INCOME** `CONTENT/social/auto_generated/alpha_content_2026_02_28.md:107` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
34. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
35. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
36. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
37. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
38. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
39. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
40. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
41. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
42. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
43. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
44. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
45. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
46. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
47. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
48. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
49. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
50. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
51. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
52. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
53. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
54. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
55. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
56. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
57. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
58. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
59. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
60. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
61. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
62. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
63. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
64. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
65. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
66. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
67. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
68. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
69. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
70. **INCOME** `CONTENT/social/shiplog/FIRST_WEEK_CONTENT.md:54` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
71. **INCOME** `CONTENT/social/shiplog/FIRST_WEEK_CONTENT.md:281` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
72. **INCOME** `CONTENT/social/shiplog/FIRST_WEEK_CONTENT.md:555` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
73. **INCOME** `CONTENT/social/shiplog/FIRST_WEEK_CONTENT.md:577` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
74. **INCOME** `CONTENT/social/shiplog/FIRST_WEEK_CONTENT.md:592` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
75. **INCOME** `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB13_C.md:55` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
76. **INCOME** `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB13_C.md:57` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
77. **INCOME** `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB13_B.md:28` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
78. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:18` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
79. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:58` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
80. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:106` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
81. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:154` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
82. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:162` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
83. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:186` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
84. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:204` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
85. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:274` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
86. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:284` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
87. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:314` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
88. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:342` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
89. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:346` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
90. **INCOME** `CONTENT/social/printmaxxer/AI_SOLOPRENEURSHIP_CONTENT_50.md:476` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
91. **INCOME** `CONTENT/social/printmaxxer/AGENT_ARCHITECTURE_RESEARCH_THREAD.md:112` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
92. **INCOME** `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB13.md:45` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
93. **INCOME** `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB13.md:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
94. **INCOME** `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB13.md:137` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
95. **INCOME** `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB13.md:151` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
96. **INCOME** `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB13.md:170` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
97. **INCOME** `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB12.md:17` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
98. **INCOME** `CONTENT/social/printmaxxer/SESSION_SQUEEZE_FEB12.md:77` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
99. **INCOME** `CONTENT/social/esoteric/FIRST_WEEK_CONTENT.md:291` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
100. **INCOME** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:20` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
101. **INCOME** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:23` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
102. **INCOME** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:166` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
103. **INCOME** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:170` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
104. **INCOME** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:184` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
105. **INCOME** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:215` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
106. **INCOME** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:221` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
107. **INCOME** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:325` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
108. **INCOME** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:340` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
109. **INCOME** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:717` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
110. **INCOME** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:763` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
111. **PII** `CONTENT/social/outboundtwts/FIRST_WEEK_CONTENT.md:485` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
112. **INCOME** `CONTENT/social/memes/MEME_BATCH_100.md:67` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
113. **INCOME** `CONTENT/social/memes/MEME_BATCH_100.md:93` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
114. **INCOME** `CONTENT/social/memes/MEME_BATCH_100.md:131` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
115. **INCOME** `CONTENT/social/pinterest/PINTEREST_PINS_50.md:353` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
116. **INCOME** `CONTENT/social/pinterest/PINTEREST_PINS_50.md:354` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
117. **INCOME** `CONTENT/social/pinterest/PINTEREST_PINS_50.md:355` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
118. **INCOME** `CONTENT/social/pinterest/PINTEREST_PINS_50.md:356` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
119. **INCOME** `CONTENT/social/pinterest/PINTEREST_PINS_50.md:386` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
120. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:19` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
121. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:21` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
122. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:27` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
123. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:37` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
124. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:39` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
125. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:59` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
126. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:85` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
127. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:111` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
128. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:143` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
129. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:149` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
130. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:153` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
131. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:161` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
132. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:171` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
133. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:175` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
134. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:181` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
135. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:211` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
136. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:215` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
137. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:219` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
138. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:221` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
139. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:253` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
140. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:279` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
141. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:295` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
142. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:299` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
143. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:307` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
144. **INCOME** `CONTENT/social/toolstwts/FIRST_WEEK_CONTENT.md:412` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
145. **INCOME** `CONTENT/social/growthpilled/FIRST_WEEK_CONTENT.md:107` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
146. **INCOME** `CONTENT/social/growthpilled/FIRST_WEEK_CONTENT.md:217` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
147. **INCOME** `CONTENT/social/growthpilled/FIRST_WEEK_CONTENT.md:229` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
148. **INCOME** `CONTENT/social/growthpilled/FIRST_WEEK_CONTENT.md:241` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
149. **INCOME** `CONTENT/social/quote_tweets/quotes_drifthour_20260302_210635.csv:37` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
150. **INCOME** `CONTENT/social/quote_tweets/quotes_drifthour_20260302_210635.csv:43` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
151. **INCOME** `CONTENT/social/repscheme/TWEET_BATCH_2026_03_02.md:23` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
152. **INCOME** `CONTENT/social/repscheme/FIRST_WEEK_CONTENT.md:24` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
153. **INCOME** `CONTENT/social/repscheme/FIRST_WEEK_CONTENT.md:108` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
154. **INCOME** `CONTENT/social/repscheme/FIRST_WEEK_CONTENT.md:451` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
155. **INCOME** `CONTENT/social/repscheme/FIRST_WEEK_CONTENT.md:505` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
156. **CANSPAM** `CONTENT/social/ramadan/ramadan_influencer_outreach.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
157. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:7` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
158. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:10` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
159. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:13` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
160. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:16` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
161. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:22` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
162. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:91` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
163. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:94` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
164. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:97` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
165. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:100` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
166. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:103` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
167. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:113` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
168. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:116` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
169. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:131` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
170. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:138` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
171. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:156` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
172. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:187` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
173. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:195` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
174. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:198` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
175. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:207` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
176. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:213` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
177. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:216` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
178. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:223` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
179. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:226` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
180. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:229` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
181. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:232` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
182. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:235` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
183. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:241` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
184. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:310` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
185. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:313` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
186. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:316` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
187. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:329` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
188. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:335` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
189. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:348` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
190. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:351` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
191. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:363` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
192. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:401` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
193. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:419` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
194. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:476` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
195. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:479` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
196. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:482` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
197. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:485` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
198. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:491` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
199. **INCOME** `CONTENT/social/threads/PRINTMAXXER_THREADS_20.md:497` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
200. **INCOME** `CONTENT/social/ai/TWEETS_FEB12.md:107` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
201. **INCOME** `CONTENT/social/ai/TWEETS_FEB12_SESSION2.md:29` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
202. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:144` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
203. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:171` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
204. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:231` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
205. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:296` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
206. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:330` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
207. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:424` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
208. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:425` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
209. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:520` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
210. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:540` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
211. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:541` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
212. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:542` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
213. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:549` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
214. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:550` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
215. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:551` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
216. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:553` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
217. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:556` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
218. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:583` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
219. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:611` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
220. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:612` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
221. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:613` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
222. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:682` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
223. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:720` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
224. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:817` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
225. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:932` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
226. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:952` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
227. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:954` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
228. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:956` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
229. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:963` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
230. **INCOME** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:1049` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
231. **PII** `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:662` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
232. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:146` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
233. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:150` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
234. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:220` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
235. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:244` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
236. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:329` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
237. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:398` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
238. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:403` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
239. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:607` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
240. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:641` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
241. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:643` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
242. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:644` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
243. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:645` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
244. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:646` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
245. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:648` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
246. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:661` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
247. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:966` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
248. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:967` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
249. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:968` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
250. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:982` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
251. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:983` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
252. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:984` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
253. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:985` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
254. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1006` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
255. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1016` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
256. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1073` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
257. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1085` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
258. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1103` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
259. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1130` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
260. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1132` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
261. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1134` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
262. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1168` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
263. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1169` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
264. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1179` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
265. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1182` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
266. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1240` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
267. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1245` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
268. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1250` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
269. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1260` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
270. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1263` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
271. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1321` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
272. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1324` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
273. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1370` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
274. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1442` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
275. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1443` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
276. **INCOME** `CONTENT/social/reddit/REDDIT_POSTS_30.md:1444` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
277. **INCOME** `CONTENT/social/fitness/FITNESS_CONTENT_50.md:18` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
278. **INCOME** `CONTENT/social/fitness/FITNESS_CONTENT_50.md:48` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
279. **INCOME** `CONTENT/social/fitness/FITNESS_CONTENT_50.md:162` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
280. **INCOME** `CONTENT/social/fitness/FITNESS_CONTENT_50.md:207` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
281. **INCOME** `CONTENT/social/drifthour/TWEET_BATCH_2026_03_02.md:45` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
282. **INCOME** `CONTENT/social/launch_posts/tech_gumroad_launch.md:109` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
283. **INCOME** `CONTENT/social/launch_posts/tech_gumroad_launch.md:189` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
284. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:27` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
285. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:54` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
286. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:79` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
287. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:80` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
288. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:81` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
289. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:176` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
290. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:270` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
291. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:272` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
292. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:273` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
293. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:274` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
294. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:291` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
295. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:358` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
296. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:426` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
297. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:510` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
298. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:587` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
299. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:588` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
300. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:611` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
301. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:612` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
302. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:820` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
303. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:821` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
304. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:822` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
305. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:823` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
306. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:827` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
307. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:828` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
308. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:829` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
309. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:830` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
310. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:832` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
311. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:852` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
312. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:951` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
313. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:953` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
314. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:957` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
315. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:959` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
316. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:961` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
317. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:963` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
318. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:964` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
319. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:966` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
320. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:968` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
321. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:970` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
322. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:972` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
323. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:978` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
324. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:979` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
325. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:981` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
326. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:985` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
327. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:987` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
328. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:989` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
329. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:991` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
330. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:995` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
331. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:999` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
332. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:1181` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
333. **INCOME** `CONTENT/social/linkedin/LINKEDIN_POSTS_30.md:1192` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
334. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
335. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
336. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
337. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
338. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
339. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_005709.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
340. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
341. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
342. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
343. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
344. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
345. **INCOME** `CONTENT/social/auto_generated/auto_content_20260216_054121.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
346. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
347. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
348. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
349. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
350. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
351. **INCOME** `CONTENT/social/auto_generated/auto_content_20260224_054118.csv:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
352. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
353. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
354. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
355. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
356. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
357. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_031727.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
358. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
359. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
360. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
361. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
362. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
363. **INCOME** `CONTENT/social/auto_generated/auto_content_20260221_054119.csv:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
364. **INCOME** `CONTENT/social/auto_generated/alpha_content_2026_02_28.md:45` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
365. **INCOME** `CONTENT/social/auto_generated/alpha_content_2026_02_28.md:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
366. **INCOME** `CONTENT/social/auto_generated/alpha_content_2026_02_28.md:107` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
367. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
368. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
369. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
370. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
371. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
372. **INCOME** `CONTENT/social/auto_generated/auto_content_20260219_054118.csv:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
373. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
374. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
375. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
376. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
377. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
378. **INCOME** `CONTENT/social/auto_generated/auto_content_20260223_054118.csv:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
379. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
380. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
381. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
382. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
383. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
384. **INCOME** `CONTENT/social/auto_generated/auto_content_20260217_054117.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
385. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
386. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
387. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
388. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
389. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
390. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_185306.csv:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
391. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
392. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
393. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
394. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
395. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
396. **INCOME** `CONTENT/social/auto_generated/auto_content_20260213_191957.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
397. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:4` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
398. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
399. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
400. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:56` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
401. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:65` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
402. **INCOME** `CONTENT/social/auto_generated/auto_content_20260214_035158.csv:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
403. **INCOME** `AUTOMATIONS/outreach/FREELANCE_RESPONSES.md:46` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
404. **INCOME** `AUTOMATIONS/outreach/FREELANCE_RESPONSES.md:48` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
405. **INCOME** `AUTOMATIONS/outreach/FREELANCE_RESPONSES.md:49` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
406. **INCOME** `AUTOMATIONS/outreach/FREELANCE_RESPONSES.md:68` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
407. **INCOME** `AUTOMATIONS/outreach/FREELANCE_RESPONSES.md:123` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
408. **CANSPAM** `AUTOMATIONS/outreach/FREELANCE_RESPONSES.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
409. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:10` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
410. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:51` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
411. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
412. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:133` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
413. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:174` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
414. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:215` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
415. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:256` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
416. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:297` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
417. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:338` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
418. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:379` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
419. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:420` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
420. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:461` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
421. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:502` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
422. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:777` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
423. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:2378` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
424. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:4564` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
425. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:5073` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
426. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:5504` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
427. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:6364` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
428. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:6873` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
429. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:7499` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
430. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:8437` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
431. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:9336` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
432. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:10196` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
433. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:11329` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
434. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:11994` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
435. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:12035` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
436. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:12622` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
437. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:13482` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
438. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:13523` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
439. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:13564` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
440. **INCOME** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:13605` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
441. **CANSPAM** `AUTOMATIONS/outreach/HOT_BATCH_FEB13_COMPLIANT.csv:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
442. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Austin_TX_The_Best_Restaurants_in_Austin_Texas.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
443. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Durants_Steakhouse.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
444. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Best_Plumbers_in_Miami_Florida.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
445. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Plumbers_in_Miami_FL_-_Rapid.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
446. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Austin_TX_Best_Restaurants_in_Austin_Fall_2025.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
447. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Catering_Downtown_Phoenix__Arcadia.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
448. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Carbone_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
449. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Best_Miami_Florida_Law_Firms.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
450. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Port_of_Miami_hotels_with_cruise_shuttle.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
451. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Free_Attorneys_Near_Me_in_Miami_Florida.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
452. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Downtown_Mountain_View_Restaurants_in_Ph.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
453. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Firebirds_Wood_Fired_Grill.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
454. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Best_Miami_Florida_Lawyers.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
455. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_The_Best_Restaurants_in_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
456. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Miami_Plumber__AC_Repair.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
457. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_MDSO_All_clear_given_after_hoax_call_of_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
458. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Find_a_lawyer_for_affordable_legal_aid.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
459. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Phoenixs_Best_Dinner_Updated_2026.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
460. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Criminal_Records.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
461. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Local_-_WSVN_7News.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
462. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Miami_MICHELIN_Restaurants.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
463. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Where_Should_I_Eat_28_Phoenix_Restaurant.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
464. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_ADMINISTRATIVE_LAW_JUDGE.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
465. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_23_Best_Plumbers_in_Phoenix_AZ_for_2026.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
466. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_US_Attorneys.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
467. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Arizona_State_Bar_Member_Directory.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
468. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Austin_TX_The_25_Best_Restaurants_In_Austin_-_Aust.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
469. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Miami_FL_Lawyers__Law_Firms.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
470. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_Springs_Plumbing_-_Plumber__Drainage_Ser.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
471. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Drinking_Made_Easy_Restaurants_in_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
472. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Star_chefs_downtown_Phoenix_Mexican_rest.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
473. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Phoenix_Lawyers.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
474. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Phoenix_Dentist_in_Phoenix_AZ.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
475. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Phoenix.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
476. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Phoenix_Find_a_Dentist_Near_You_-_Trusted_Networ.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
477. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Buck__Rider_-_Seafood_Restaurant_Arizona.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
478. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Meet_The_Suzuki_Law_Offices_Legal_Team.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
479. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Videos_from_The_Cosmetic_Dentists_of_Aus.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
480. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Phoenix_VA_Dentistry.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
481. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_Blue_Cross_Blue_Shield_FEP_Dental.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
482. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_General_Dentist_in_33143.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
483. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Phoenix_Restaurant_Consulting_Services.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
484. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Office_Catering_in_Phoenix_Elevate_Your_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
485. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_GPR_Program_Miller_School_of_Medicine.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
486. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Phoenix_BEST_Life_and_Health_Insurance_Company.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
487. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Delilah.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
488. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_Relax_and_Smile_Dental_Care.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
489. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Plumber_in_Miami_FL.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
490. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_Find_Your_Local_Trusted_Dentist.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
491. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_10_Best_Rooftop_Restaurants_in_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
492. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Phoenix_and_The_Arizona_Republic_Phoenix_and_Ari.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
493. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Man_gets_25_years_for_deadly_Safeway_sta.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
494. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Top_Phoenix_office_catering_restaurants_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
495. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_The_25_Best_Restaurants_In_Miami_-_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
496. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_THE_99_BEST_Restaurants_in_Phoenix.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
497. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_MA__ASSOCIATES_PA.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
498. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_The_Best_Plumbers_in_Miami_FL.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
499. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Manuels_Mexican_Restaurant__Cantina.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
500. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_The_9_Best_Plumbers_in_Phoenix_2026.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
501. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_Phoenix_Plumbing_Technician_Training_Pro.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
502. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Floridas_Top_15_Local_Restaurants_In_Mia.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
503. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Crazy_About_You.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
504. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_16_Best_Plumbers_in_Miami_FL_for_2026.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
505. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Miami_FL_Attorneys_Near_Me.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
506. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Phoenix_Everyday_Practices_Dental_Podcast_Welcom.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
507. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Dentist_in_Austin_TX.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
508. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Austin_Primary_Dental.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
509. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Find_a_Roto.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
510. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_Journeyman_and_Apprentice_Licensing.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
511. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_The_38_Best_Restaurants_in_Phoenix.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
512. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Phoenix_Corporate_Caterers.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
513. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Plumbing_Supplies_HVAC_Parts_Pipe_Valves.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
514. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Warnerbros.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
515. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_UA_Plumbers_and_Pipefitters_Local_No_725.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
516. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Industry_Standard_Phoenixs_Top_Spot_for_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
517. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_10_Best_Restaurants_in_Phoenix_and_Scott.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
518. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Native_American_Cuisine_Restaurants.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
519. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_Modern_Judgment.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
520. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_100_Best_Restaurants_in_Miami_Florida.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
521. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Phoenix_AZ_Lawyers__Law_Firms.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
522. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Pollo_Tropical.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
523. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Austin_TX_22_Best_Restaurants_in_Austin_Brisket_Is.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
524. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_WPLG_Local_10.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
525. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Austin_TX_Austin_MICHELIN_Restaurants.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
526. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Hedgecock_Dentalhedgecockdentalcom.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
527. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_Quality_Affordable_Dental_Care.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
528. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Find_Your_Local_Medical_Malpractice_Lawy.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
529. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Home.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
530. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Ocean_Prime_Restaurant.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
531. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_2026_Guide_to_Best_Law_Firm_in_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
532. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_advanceddentalcareofaustincomDentist_Nea.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
533. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Local_Business_Tax_Receipt.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
534. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_plumbers_near_Surprise_AZ_85387.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
535. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_The_22_Hidden_Gem_Restaurants_in_Miami_B.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
536. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Hajoca.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
537. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Quality_Dentistry_Honestly_Delivered.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
538. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_These_Are_the_Best_Restaurants_in_Miami_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
539. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_Pediatric_Dentist_Near_Doral_FL.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
540. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Real_Estate_Agent_Search.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
541. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Phoenix_Arizona_Breaking_News.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
542. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Best_Law_Firms_in_Miami_FL.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
543. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Inspectors_hit_Scottsdale_ramen_restaura.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
544. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_16_Best_Restaurants_in_Phoenix_According.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
545. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Our_Locations.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
546. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Eco1Plumbing.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
547. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Broening_Oberg_Woods__Wilson_PC_recogniz.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
548. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_The_Best_Restaurants_in_Miami_and_Miami_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
549. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Bill_Dingaustexdentalcom.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
550. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_Miami_Dentists_Near_You.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
551. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Miami_Office_with_a_restaurant.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
552. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_Plumber_Phoenix.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
553. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Austin_TX_25_Best_Restaurants_in_Austin_2025.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
554. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_World-Class_Dental_Support_Organization.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
555. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_10_Best_Plumbers_in_Phoenix_AZ.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
556. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Phoenixs_Best_Lawyers_Updated_2026.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
557. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Where_to_Eat_in_Phoenix_The_Top_20_Resta.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
558. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_5_Best_Dental_Clinics_in_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
559. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Trusted_Dentist_in_Austin_TX_for_Family_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
560. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Law_Office_Receptionist_-_admin__office.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
561. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_Plumbing_Services_Phoenix_AZ.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
562. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Family_Dentist_in_Austin_TX_-_Kids_Denti.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
563. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_24-Hour_Emergency_Plumbing.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
564. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Phoenix_General_and_Cosmetic_Dentistry_-_Dental_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
565. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Dental_Implants_Austin_TX.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
566. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Phoenix_AZ_Attorneys_Near_Me.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
567. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Miami_Restaurant_Space_for_Rent.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
568. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_Plumber_Phoenix_AZ.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
569. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Commercial_Lease_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
570. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_5_metro_Phoenix_restaurants_we_wish_made.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
571. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_My_Fit_Foods.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
572. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Fast_Reliable_Services_from_a_Top_Plumbe.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
573. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_The_40_Best_Restaurants_and_Bars_in_Phoe.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
574. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Glow_Dental_Coglowdentalcocom.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
575. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Places_to_Eat_in_Miami_30_Hidden_Food_Ge.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
576. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Non-Invasive_Leak_Detection_Services.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
577. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Top_10_restaurants_for_business_meetings.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
578. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_31_Best_Restaurants_in_Miami_February_20.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
579. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Austin_TX_Horseshoe_Bay_Resort_A_Golf__Spa_Resort_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
580. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Phoenix_Arizona_Dental_Home_Page.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
581. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Miami_Office.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
582. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Slyvester_Lee_James_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
583. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Miami_Florida.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
584. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Northwestaustindentistsnorthwestaustinde.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
585. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_Dental_Practice_For_Sale_By_Owner_Guide_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
586. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_20_Best_Restaurants_in_Phoenix_AZ_2026_U.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
587. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Florida_Certified_Plumbing_Contractor_Ex.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
588. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_Plumbing__Drain_Cleaning_Services_You_Ca.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
589. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Austin_TX_Dental_Services_for_the_Whole_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
590. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Best_Phoenix_Arizona_Lawyers.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
591. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_MILA_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
592. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Best_Miami_Restaurant__Food_Service_Staf.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
593. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Versailles.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
594. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Continental_PLLC.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
595. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_Phoenix_Restaurant_Consulting.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
596. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Discover_the_Best_Plumbers_in_Miami_2025.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
597. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_About_Us.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
598. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Austin_TX_Rose_Dental_Grouprosedentalcom.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
599. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_The_38_Best_Restaurants_in_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
600. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Almazan_Law_-_South_Miami_FL.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
601. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_Miami_Dentist.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
602. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Austin_TX_The_30_Best_Restaurants_In_Austin_Right_.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
603. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Miami_Plumber.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
604. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_The_Best_Neighborhood_Italian_Restaurant.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
605. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_I_visited_Bad_Bunnys_high.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
606. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_Restaurant_Consultants_Miami.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
607. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Phoenix_Best_Phoenix_Arizona_Law_Firms.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
608. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Phoenix_Affordable_family.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
609. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_HVAC_Air_Conditioning_Heating_and_Plumbi.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
610. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Phoenix_The_13_best_restaurants_in_downtown_Phoe.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
611. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Phoenix_Dentist_Near_Me.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
612. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_Miami_Attorneys.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
613. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_Journeyman_Plumber_Exam_Preparation.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
614. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/legal_Miami_NFL_News_Scores_Standings__Stats.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
615. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_Plumber_Phoenix_AZ_-_Parker__Sons.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
616. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Miami_City_of_Philadelphia.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
617. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/dental_Miami_A_list_of_25_Dental_Conferences_2026.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
618. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/restaurant_Miami_TRG_Miami_-_TRG_Restaurant_Consultants.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
619. **CANSPAM** `AUTOMATIONS/outreach/cold_emails_txt_Austin_Miami_Phoenix/plumber_Phoenix_Best_Plumbers_Phoenix_393_Reviewed.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
620. **INCOME** `AUTOMATIONS/content_posting/MASTER_CONTENT_BATCH_FEB12.csv:11` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
621. **INCOME** `AUTOMATIONS/content_posting/MASTER_CONTENT_BATCH_FEB12.csv:13` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
622. **INCOME** `AUTOMATIONS/content_posting/MASTER_CONTENT_BATCH_FEB12.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
623. **INCOME** `AUTOMATIONS/content_posting/MASTER_CONTENT_BATCH_FEB12.csv:16` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
624. **INCOME** `AUTOMATIONS/content_posting/MASTER_CONTENT_BATCH_FEB12.csv:43` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
625. **INCOME** `AUTOMATIONS/content_posting/MASTER_CONTENT_BATCH_FEB12.csv:82` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
626. **INCOME** `AUTOMATIONS/content_posting/MASTER_CONTENT_BATCH_FEB12.csv:94` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
627. **INCOME** `AUTOMATIONS/content_posting/cold_email_subject_lines_100.csv:7` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
628. **INCOME** `AUTOMATIONS/content_posting/cold_email_subject_lines_100.csv:41` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
629. **INCOME** `AUTOMATIONS/content_posting/cold_email_subject_lines_100.csv:70` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
630. **CANSPAM** `AUTOMATIONS/content_posting/cold_email_subject_lines_100.csv:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
631. **INCOME** `AUTOMATIONS/content_posting/ecom_arb_content_30.csv:5` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
632. **INCOME** `AUTOMATIONS/content_posting/ecom_arb_content_30.csv:8` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
633. **INCOME** `AUTOMATIONS/content_posting/ecom_arb_content_30.csv:10` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
634. **INCOME** `AUTOMATIONS/content_posting/ecom_arb_content_30.csv:12` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
635. **INCOME** `AUTOMATIONS/content_posting/ecom_arb_content_30.csv:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
636. **INCOME** `AUTOMATIONS/content_posting/ecom_arb_content_30.csv:15` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
637. **INCOME** `AUTOMATIONS/content_posting/ecom_arb_content_30.csv:18` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
638. **INCOME** `AUTOMATIONS/content_posting/ecom_arb_content_30.csv:24` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
639. **INCOME** `AUTOMATIONS/content_posting/ecom_arb_content_30.csv:28` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
640. **INCOME** `AUTOMATIONS/content_posting/meme_engagement_tweets_30.csv:10` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
641. **INCOME** `AUTOMATIONS/content_posting/meme_engagement_tweets_30.csv:22` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
642. **INCOME** `AUTOMATIONS/content_posting/meme_engagement_tweets_30.csv:23` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
643. **INCOME** `AUTOMATIONS/content_posting/meme_engagement_tweets_30.csv:26` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
644. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:18` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
645. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:31` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
646. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:46` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
647. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:93` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
648. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:109` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
649. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:153` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
650. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:168` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
651. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:208` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
652. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:230` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
653. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:262` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
654. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:277` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
655. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:293` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
656. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:332` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
657. **INCOME** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:355` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
658. **CANSPAM** `AUTOMATIONS/content_posting/cold_email_sequences_ready.csv:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
659. **INCOME** `AUTOMATIONS/content_posting/findom_tweets_50.csv:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
660. **INCOME** `AUTOMATIONS/content_posting/gov_contract_tweets_50.csv:26` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
661. **INCOME** `AUTOMATIONS/content_posting/printmaxxer_tweets_50.csv:9` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
662. **INCOME** `AUTOMATIONS/content_posting/printmaxxer_tweets_50.csv:11` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
663. **INCOME** `AUTOMATIONS/content_posting/printmaxxer_tweets_50.csv:12` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
664. **INCOME** `AUTOMATIONS/content_posting/printmaxxer_tweets_50.csv:18` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
665. **INCOME** `AUTOMATIONS/content_posting/printmaxxer_tweets_50.csv:30` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
666. **INCOME** `AUTOMATIONS/content_posting/printmaxxer_tweets_50.csv:46` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
667. **INCOME** `AUTOMATIONS/content_posting/BUFFER_UPLOAD_GUIDE.md:143` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
668. **INCOME** `AUTOMATIONS/content_posting/BUFFER_UPLOAD_GUIDE.md:191` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
669. **INCOME** `AUTOMATIONS/content_posting/BUFFER_UPLOAD_GUIDE.md:262` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
670. **INCOME** `AUTOMATIONS/content_posting/BUFFER_UPLOAD_GUIDE.md:271` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
671. **INCOME** `AUTOMATIONS/content_posting/BUFFER_UPLOAD_GUIDE.md:509` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
672. **INCOME** `AUTOMATIONS/content_posting/BUFFER_UPLOAD_GUIDE.md:526` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
673. **INCOME** `AUTOMATIONS/content_posting/BUFFER_UPLOAD_GUIDE.md:727` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
674. **INCOME** `AUTOMATIONS/content_posting/BUFFER_UPLOAD_GUIDE.md:743` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
675. **INCOME** `AUTOMATIONS/content_posting/BUFFER_UPLOAD_GUIDE.md:744` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
676. **INCOME** `AUTOMATIONS/content_posting/BUFFER_UPLOAD_GUIDE.md:745` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
677. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_shiplog_twitter.csv:136` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
678. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_shiplog_twitter.csv:175` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
679. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_shiplog_twitter.csv:192` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
680. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_shiplog_twitter.csv:243` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
681. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_clipvault_instagram.csv:206` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
682. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_clipvault_instagram.csv:334` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
683. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_clipvault_instagram.csv:438` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
684. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_printmaxxer_linkedin.csv:170` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
685. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_printmaxxer_linkedin.csv:454` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
686. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_clipvault_twitter.csv:33` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
687. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_clipvault_twitter.csv:42` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
688. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_clipvault_twitter.csv:63` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
689. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_printmaxxer_reddit.csv:66` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
690. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_printmaxxer_reddit.csv:158` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
691. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_printmaxxer_reddit.csv:190` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
692. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_printmaxxer_reddit.csv:211` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
693. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_growthpilled_linkedin.csv:176` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
694. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_growthpilled_linkedin.csv:460` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
695. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_twitter.csv:2` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
696. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_twitter.csv:18` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
697. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_twitter.csv:63` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
698. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_twitter.csv:76` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
699. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_twitter.csv:151` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
700. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_twitter.csv:163` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
701. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_instagram.csv:44` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
702. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_instagram.csv:142` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
703. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_instagram.csv:144` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
704. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_instagram.csv:146` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
705. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_instagram.csv:445` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
706. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_instagram.csv:447` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
707. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_instagram.csv:449` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
708. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_instagram.csv:451` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
709. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_instagram.csv:562` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
710. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_outboundtwts_linkedin.csv:174` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
711. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_outboundtwts_linkedin.csv:450` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
712. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_clipvault_tiktok.csv:78` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
713. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_clipvault_tiktok.csv:126` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
714. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_clipvault_tiktok.csv:168` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
715. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_printmaxxer_twitter.csv:136` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
716. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_printmaxxer_twitter.csv:175` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
717. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_printmaxxer_twitter.csv:192` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
718. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_printmaxxer_twitter.csv:243` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
719. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_outboundtwts_twitter.csv:136` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
720. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_outboundtwts_twitter.csv:175` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
721. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_outboundtwts_twitter.csv:192` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
722. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_outboundtwts_twitter.csv:243` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
723. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_growthpilled_twitter.csv:136` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
724. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_growthpilled_twitter.csv:175` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
725. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_growthpilled_twitter.csv:192` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
726. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_growthpilled_twitter.csv:243` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
727. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_tiktok.csv:16` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
728. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_tiktok.csv:46` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
729. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_tiktok.csv:181` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
730. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_repscheme_tiktok.csv:232` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
731. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_toolstwts_twitter.csv:136` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
732. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_toolstwts_twitter.csv:175` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
733. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_toolstwts_twitter.csv:192` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
734. **INCOME** `AUTOMATIONS/content_posting/buffer_exports/buffer_toolstwts_twitter.csv:243` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
735. **INCOME** `AUTOMATIONS/freelance_response_templates/09_freelance_designer_20hrs_week.md:1` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
736. **INCOME** `AUTOMATIONS/freelance_response_templates/09_freelance_designer_20hrs_week.md:7` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
737. **INCOME** `AUTOMATIONS/freelance_response_templates/09_freelance_designer_20hrs_week.md:16` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
738. **INCOME** `AUTOMATIONS/freelance_response_templates/09_freelance_designer_20hrs_week.md:20` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
739. **INCOME** `AUTOMATIONS/freelance_response_templates/09_freelance_designer_20hrs_week.md:69` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
740. **INCOME** `AUTOMATIONS/freelance_response_templates/09_freelance_designer_20hrs_week.md:79` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
741. **INCOME** `AUTOMATIONS/freelance_response_templates/INDEX.md:27` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
742. **INCOME** `AUTOMATIONS/freelance_response_templates/INDEX.md:36` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
743. **INCOME** `AUTOMATIONS/freelance_response_templates/INDEX.md:37` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
744. **INCOME** `AUTOMATIONS/freelance_response_templates/INDEX.md:67` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
745. **INCOME** `AUTOMATIONS/freelance_response_templates/INDEX.md:70` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
746. **INCOME** `AUTOMATIONS/freelance_response_templates/INDEX.md:71` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
747. **INCOME** `AUTOMATIONS/freelance_response_templates/INDEX.md:72` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
748. **INCOME** `AUTOMATIONS/freelance_response_templates/07_operations_assistant_20hr.md:1` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
749. **INCOME** `AUTOMATIONS/freelance_response_templates/07_operations_assistant_20hr.md:7` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
750. **INCOME** `AUTOMATIONS/freelance_response_templates/07_operations_assistant_20hr.md:16` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
751. **INCOME** `AUTOMATIONS/freelance_response_templates/07_operations_assistant_20hr.md:20` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
752. **INCOME** `AUTOMATIONS/freelance_response_templates/07_operations_assistant_20hr.md:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
753. **INCOME** `AUTOMATIONS/freelance_response_templates/07_operations_assistant_20hr.md:66` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
754. **INCOME** `AUTOMATIONS/freelance_response_templates/07_operations_assistant_20hr.md:76` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
755. **INCOME** `PRODUCTS/KDP_JOURNALS_10.md:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
756. **INCOME** `PRODUCTS/KDP_JOURNALS_10.md:22` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
757. **INCOME** `PRODUCTS/MERCARI_EBAY_ARB.md:166` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
758. **INCOME** `PRODUCTS/funnel_teardown_guide.md:34` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
759. **INCOME** `PRODUCTS/funnel_teardown_guide.md:45` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
760. **INCOME** `PRODUCTS/funnel_teardown_guide.md:60` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
761. **INCOME** `PRODUCTS/funnel_teardown_guide.md:94` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
762. **INCOME** `PRODUCTS/funnel_teardown_guide.md:97` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
763. **INCOME** `PRODUCTS/funnel_teardown_guide.md:100` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
764. **INCOME** `PRODUCTS/funnel_teardown_guide.md:108` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
765. **INCOME** `PRODUCTS/funnel_teardown_guide.md:118` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
766. **INCOME** `PRODUCTS/funnel_teardown_guide.md:120` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
767. **INCOME** `PRODUCTS/funnel_teardown_guide.md:138` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
768. **INCOME** `PRODUCTS/funnel_teardown_guide.md:140` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
769. **INCOME** `PRODUCTS/funnel_teardown_guide.md:170` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
770. **INCOME** `PRODUCTS/funnel_teardown_guide.md:210` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
771. **INCOME** `PRODUCTS/funnel_teardown_guide.md:220` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
772. **INCOME** `PRODUCTS/funnel_teardown_guide.md:254` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
773. **INCOME** `PRODUCTS/funnel_teardown_guide.md:271` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
774. **INCOME** `PRODUCTS/funnel_teardown_guide.md:273` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
775. **INCOME** `PRODUCTS/funnel_teardown_guide.md:275` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
776. **INCOME** `PRODUCTS/funnel_teardown_guide.md:277` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
777. **INCOME** `PRODUCTS/funnel_teardown_guide.md:283` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
778. **INCOME** `PRODUCTS/funnel_teardown_guide.md:289` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
779. **INCOME** `PRODUCTS/funnel_teardown_guide.md:320` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
780. **INCOME** `PRODUCTS/funnel_teardown_guide.md:330` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
781. **INCOME** `PRODUCTS/funnel_teardown_guide.md:332` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
782. **INCOME** `PRODUCTS/funnel_teardown_guide.md:338` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
783. **INCOME** `PRODUCTS/funnel_teardown_guide.md:354` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
784. **INCOME** `PRODUCTS/funnel_teardown_guide.md:394` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
785. **INCOME** `PRODUCTS/funnel_teardown_guide.md:412` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
786. **INCOME** `PRODUCTS/ai_automation_toolkit.md:64` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
787. **INCOME** `PRODUCTS/ai_automation_toolkit.md:195` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
788. **INCOME** `PRODUCTS/ai_automation_toolkit.md:321` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
789. **INCOME** `PRODUCTS/ai_automation_toolkit.md:328` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
790. **INCOME** `PRODUCTS/ai_automation_toolkit.md:492` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
791. **INCOME** `PRODUCTS/ai_automation_toolkit.md:566` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
792. **INCOME** `PRODUCTS/ai_automation_toolkit.md:725` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
793. **INCOME** `PRODUCTS/ai_automation_toolkit.md:731` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
794. **INCOME** `PRODUCTS/ai_automation_toolkit.md:907` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
795. **INCOME** `PRODUCTS/ai_automation_toolkit.md:1195` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
796. **INCOME** `PRODUCTS/ai_automation_toolkit.md:1447` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
797. **INCOME** `PRODUCTS/ai_automation_toolkit.md:1562` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
798. **INCOME** `PRODUCTS/ai_automation_toolkit.md:1567` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
799. **INCOME** `PRODUCTS/ai_automation_toolkit.md:1572` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
800. **PII** `PRODUCTS/ai_automation_toolkit.md:739` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
801. **PII** `PRODUCTS/ai_automation_toolkit.md:740` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
802. **PII** `PRODUCTS/ai_automation_toolkit.md:754` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
803. **PII** `PRODUCTS/ai_automation_toolkit.md:776` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
804. **PII** `PRODUCTS/ai_automation_toolkit.md:983` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
805. **INCOME** `PRODUCTS/ECOM_UPLOAD_CHECKLIST.md:98` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
806. **INCOME** `PRODUCTS/ECOM_UPLOAD_CHECKLIST.md:99` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
807. **INCOME** `PRODUCTS/ECOM_UPLOAD_CHECKLIST.md:100` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
808. **INCOME** `PRODUCTS/ECOM_UPLOAD_CHECKLIST.md:134` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
809. **INCOME** `PRODUCTS/ECOM_UPLOAD_CHECKLIST.md:326` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
810. **INCOME** `PRODUCTS/ECOM_UPLOAD_CHECKLIST.md:380` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
811. **INCOME** `PRODUCTS/ECOM_UPLOAD_CHECKLIST.md:381` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
812. **INCOME** `PRODUCTS/ECOM_UPLOAD_CHECKLIST.md:383` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
813. **INCOME** `PRODUCTS/ECOM_UPLOAD_CHECKLIST.md:385` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
814. **PII** `PRODUCTS/VIBE_CODER_SECURITY_CHECKLIST.md:294` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
815. **INCOME** `PRODUCTS/REDBUBBLE_LISTINGS.md:635` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
816. **INCOME** `PRODUCTS/vibe_coding_playbook.md:23` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
817. **INCOME** `PRODUCTS/vibe_coding_playbook.md:90` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
818. **INCOME** `PRODUCTS/vibe_coding_playbook.md:98` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
819. **INCOME** `PRODUCTS/vibe_coding_playbook.md:116` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
820. **INCOME** `PRODUCTS/vibe_coding_playbook.md:181` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
821. **INCOME** `PRODUCTS/vibe_coding_playbook.md:376` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
822. **INCOME** `PRODUCTS/vibe_coding_playbook.md:390` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
823. **INCOME** `PRODUCTS/vibe_coding_playbook.md:391` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
824. **INCOME** `PRODUCTS/vibe_coding_playbook.md:564` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
825. **INCOME** `PRODUCTS/vibe_coding_playbook.md:644` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
826. **INCOME** `PRODUCTS/vibe_coding_playbook.md:648` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
827. **INCOME** `PRODUCTS/vibe_coding_playbook.md:743` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
828. **INCOME** `PRODUCTS/vibe_coding_playbook.md:744` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
829. **INCOME** `PRODUCTS/vibe_coding_playbook.md:745` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
830. **INCOME** `PRODUCTS/vibe_coding_playbook.md:746` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
831. **INCOME** `PRODUCTS/vibe_coding_playbook.md:747` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
832. **INCOME** `PRODUCTS/vibe_coding_playbook.md:754` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
833. **INCOME** `PRODUCTS/vibe_coding_playbook.md:943` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
834. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1034` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
835. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1140` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
836. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1311` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
837. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1312` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
838. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1345` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
839. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1346` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
840. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1347` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
841. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1348` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
842. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1349` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
843. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1350` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
844. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1351` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
845. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1352` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
846. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1353` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
847. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1356` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
848. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1357` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
849. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1358` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
850. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1359` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
851. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1360` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
852. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1361` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
853. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1362` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
854. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1363` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
855. **INCOME** `PRODUCTS/vibe_coding_playbook.md:1364` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
856. **INCOME** `PRODUCTS/sleep_youtube_starter.md:149` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
857. **INCOME** `PRODUCTS/sleep_youtube_starter.md:386` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
858. **INCOME** `PRODUCTS/ai_content_farm_blueprint.md:34` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
859. **INCOME** `PRODUCTS/ai_content_farm_blueprint.md:35` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
860. **INCOME** `PRODUCTS/ai_content_farm_blueprint.md:338` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
861. **INCOME** `PRODUCTS/ai_content_farm_blueprint.md:343` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
862. **INCOME** `PRODUCTS/cold_email_playbook.md:11` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
863. **INCOME** `PRODUCTS/cold_email_playbook.md:105` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
864. **INCOME** `PRODUCTS/cold_email_playbook.md:112` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
865. **INCOME** `PRODUCTS/cold_email_playbook.md:118` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
866. **INCOME** `PRODUCTS/cold_email_playbook.md:124` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
867. **INCOME** `PRODUCTS/cold_email_playbook.md:148` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
868. **INCOME** `PRODUCTS/cold_email_playbook.md:149` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
869. **INCOME** `PRODUCTS/cold_email_playbook.md:280` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
870. **INCOME** `PRODUCTS/cold_email_playbook.md:313` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
871. **INCOME** `PRODUCTS/cold_email_playbook.md:457` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
872. **INCOME** `PRODUCTS/cold_email_playbook.md:482` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
873. **INCOME** `PRODUCTS/cold_email_playbook.md:484` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
874. **INCOME** `PRODUCTS/cold_email_playbook.md:506` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
875. **INCOME** `PRODUCTS/cold_email_playbook.md:848` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
876. **INCOME** `PRODUCTS/cold_email_playbook.md:882` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
877. **INCOME** `PRODUCTS/ETSY_LISTINGS_20.md:112` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
878. **INCOME** `PRODUCTS/ETSY_LISTINGS_20.md:122` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
879. **INCOME** `PRODUCTS/ETSY_LISTINGS_20.md:209` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
880. **INCOME** `PRODUCTS/ETSY_LISTINGS_20.md:217` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
881. **INCOME** `PRODUCTS/ETSY_LISTINGS_20.md:280` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
882. **INCOME** `PRODUCTS/ETSY_LISTINGS_20.md:362` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
883. **INCOME** `PRODUCTS/ETSY_LISTINGS_20.md:387` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
884. **INCOME** `PRODUCTS/ETSY_LISTINGS_20.md:396` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
885. **INCOME** `PRODUCTS/ETSY_LISTINGS_20.md:464` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
886. **INCOME** `PRODUCTS/UPLOAD_CHECKLIST.md:121` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
887. **INCOME** `PRODUCTS/local_biz_client_system.md:502` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
888. **INCOME** `PRODUCTS/local_biz_client_system.md:503` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
889. **INCOME** `PRODUCTS/local_biz_client_system.md:504` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
890. **INCOME** `PRODUCTS/local_biz_client_system.md:507` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
891. **INCOME** `PRODUCTS/local_biz_client_system.md:510` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
892. **INCOME** `PRODUCTS/local_biz_client_system.md:536` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
893. **INCOME** `PRODUCTS/local_biz_client_system.md:553` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
894. **INCOME** `PRODUCTS/GUMROAD_READY_LISTINGS.md:85` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
895. **INCOME** `PRODUCTS/GUMROAD_READY_LISTINGS.md:102` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
896. **INCOME** `PRODUCTS/GUMROAD_READY_LISTINGS.md:189` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
897. **INCOME** `PRODUCTS/GUMROAD_READY_LISTINGS.md:250` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
898. **INCOME** `PRODUCTS/GUMROAD_READY_LISTINGS.md:341` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
899. **INCOME** `PRODUCTS/GUMROAD_READY_LISTINGS.md:369` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
900. **INCOME** `PRODUCTS/GUMROAD_READY_LISTINGS.md:387` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
901. **INCOME** `PRODUCTS/GUMROAD_READY_LISTINGS.md:446` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
902. **INCOME** `PRODUCTS/GUMROAD_READY_LISTINGS.md:454` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
903. **INCOME** `PRODUCTS/POD_DESIGNS_50.md:19` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
904. **INCOME** `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md:95` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
905. **INCOME** `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md:177` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
906. **INCOME** `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md:304` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
907. **INCOME** `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md:305` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
908. **INCOME** `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md:306` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
909. **INCOME** `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md:307` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
910. **INCOME** `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md:308` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
911. **INCOME** `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md:338` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
912. **INCOME** `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md:540` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
913. **INCOME** `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md:550` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
914. **INCOME** `PRODUCTS/PRODUCTS_CENTRAL_INDEX.md:664` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
915. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:9` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
916. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:21` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
917. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:55` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
918. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
919. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:76` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
920. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:87` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
921. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:90` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
922. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
923. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:96` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
924. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:97` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
925. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:106` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
926. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:125` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
927. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:130` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
928. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:139` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
929. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:144` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
930. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:148` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
931. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:149` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
932. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:150` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
933. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:159` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
934. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:179` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
935. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:181` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
936. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:183` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
937. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:187` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
938. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:188` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
939. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:189` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
940. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:194` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
941. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:195` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
942. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:196` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
943. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:197` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
944. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:198` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
945. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:206` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
946. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:217` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
947. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:219` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
948. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:224` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
949. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:226` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
950. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:233` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
951. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:243` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
952. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:251` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
953. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:257` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
954. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:259` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
955. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:267` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
956. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:279` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
957. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:294` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
958. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:300` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
959. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:301` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
960. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:306` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
961. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:307` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
962. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:308` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
963. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:312` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
964. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:323` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
965. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:335` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
966. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:341` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
967. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:349` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
968. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:361` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
969. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:375` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
970. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:381` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
971. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:383` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
972. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:387` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
973. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:398` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
974. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:436` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
975. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:453` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
976. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:461` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
977. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:477` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
978. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:489` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
979. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:491` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
980. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:497` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
981. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:503` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
982. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:513` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
983. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:517` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
984. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:532` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
985. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:537` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
986. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:570` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
987. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:572` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
988. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:590` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
989. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:592` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
990. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:610` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
991. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:647` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
992. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:648` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
993. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:650` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
994. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:651` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
995. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:652` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
996. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:653` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
997. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:663` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
998. **INCOME** `PRODUCTS/solopreneur_tech_stack.md:676` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
999. **INCOME** `PRODUCTS/POD_DESIGNS_20.md:21` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1000. **INCOME** `PRODUCTS/POD_DESIGNS_20.md:22` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1001. **INCOME** `PRODUCTS/POD_DESIGNS_20.md:23` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1002. **INCOME** `PRODUCTS/POD_DESIGNS_20.md:24` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1003. **INCOME** `PRODUCTS/POD_DESIGNS_20.md:25` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1004. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:67` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1005. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:72` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1006. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:78` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1007. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:85` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1008. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:314` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1009. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:319` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1010. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:326` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1011. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:333` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1012. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:562` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1013. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:567` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1014. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:573` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1015. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:580` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1016. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:785` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1017. **INCOME** `PRODUCTS/branding/FINDOM_PERSONAS.md:786` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1018. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:5` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1019. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:42` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1020. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:49` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1021. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:89` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1022. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:240` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1023. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:247` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1024. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:293` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1025. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:342` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1026. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:399` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1027. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:400` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1028. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:401` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1029. **INCOME** `PRODUCTS/branding/NEWSLETTER_BRANDS.md:418` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1030. **INCOME** `PRODUCTS/branding/MEME_ACCOUNTS.md:148` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1031. **INCOME** `PRODUCTS/branding/MEME_ACCOUNTS.md:178` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1032. **INCOME** `PRODUCTS/branding/MEME_ACCOUNTS.md:194` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1033. **INCOME** `PRODUCTS/branding/MEME_ACCOUNTS.md:209` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1034. **INCOME** `PRODUCTS/branding/MEME_ACCOUNTS.md:230` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1035. **INCOME** `PRODUCTS/branding/MEME_ACCOUNTS.md:232` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1036. **INCOME** `PRODUCTS/branding/MEME_ACCOUNTS.md:240` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1037. **INCOME** `PRODUCTS/branding/MEME_ACCOUNTS.md:254` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1038. **INCOME** `PRODUCTS/branding/PRINTMAXX_3NICHE_BRAND_SYSTEM.md:112` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1039. **INCOME** `PRODUCTS/branding/PRINTMAXX_3NICHE_BRAND_SYSTEM.md:135` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1040. **INCOME** `PRODUCTS/branding/PRINTMAXX_3NICHE_BRAND_SYSTEM.md:136` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1041. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:3` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1042. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:492` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1043. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:493` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1044. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:494` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1045. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:495` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1046. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:496` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1047. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:509` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1048. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:513` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1049. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:538` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1050. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:539` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1051. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:541` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1052. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:542` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1053. **INCOME** `PRODUCTS/branding/CONTENT_FARM_CHANNELS.md:543` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1054. **INCOME** `PRODUCTS/branding/PRINTMAXXER_BRAND_IDENTITY.md:64` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1055. **INCOME** `PRODUCTS/branding/PRINTMAXXER_BRAND_IDENTITY.md:193` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1056. **INCOME** `PRODUCTS/branding/PRINTMAXXER_BRAND_IDENTITY.md:208` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1057. **INCOME** `PRODUCTS/branding/PRINTMAXXER_BRAND_IDENTITY.md:256` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1058. **INCOME** `PRODUCTS/branding/PRINTMAXXER_BRAND_IDENTITY.md:259` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1059. **INCOME** `PRODUCTS/branding/PRINTMAXXER_BRAND_IDENTITY.md:282` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1060. **INCOME** `PRODUCTS/branding/PRINTMAXXER_BRAND_IDENTITY.md:318` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1061. **INCOME** `PRODUCTS/branding/PRINTMAXXER_BRAND_IDENTITY.md:325` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1062. **INCOME** `PRODUCTS/branding/BUSINESS_ACCOUNTS.md:71` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1063. **INCOME** `PRODUCTS/branding/BUSINESS_ACCOUNTS.md:163` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1064. **INCOME** `PRODUCTS/ETSY_INSTANT_UPLOAD/ETSY_LISTINGS_ALL.md:81` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1065. **INCOME** `PRODUCTS/ETSY_INSTANT_UPLOAD/ETSY_LISTINGS_ALL.md:91` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1066. **INCOME** `PRODUCTS/ETSY_INSTANT_UPLOAD/ETSY_LISTINGS_ALL.md:139` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1067. **INCOME** `PRODUCTS/ETSY_INSTANT_UPLOAD/ETSY_LISTINGS_ALL.md:146` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1068. **INCOME** `PRODUCTS/ETSY_INSTANT_UPLOAD/ETSY_LISTINGS_ALL.md:192` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1069. **INCOME** `PRODUCTS/ETSY_INSTANT_UPLOAD/ETSY_LISTINGS_ALL.md:240` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1070. **INCOME** `PRODUCTS/ETSY_INSTANT_UPLOAD/ETSY_LISTINGS_ALL.md:263` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1071. **INCOME** `PRODUCTS/ETSY_INSTANT_UPLOAD/ETSY_LISTINGS_ALL.md:268` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1072. **INCOME** `PRODUCTS/ETSY_INSTANT_UPLOAD/ETSY_LISTINGS_ALL.md:308` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1073. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/GIG_10_DATA_ANALYSIS.md:72` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1074. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/GIG_08_APP_DEVELOPMENT.md:59` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1075. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/GIG_08_APP_DEVELOPMENT.md:122` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1076. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/GIG_05_AUTOMATION.md:111` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1077. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/FIVERR_METADATA.md:142` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1078. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/FIVERR_METADATA.md:143` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1079. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/FIVERR_METADATA.md:144` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1080. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/FIVERR_METADATA.md:145` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1081. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/FIVERR_METADATA.md:146` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1082. **CANSPAM** `PRODUCTS/FIVERR_INSTANT_UPLOAD/GIG_03_COLD_EMAIL.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1083. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/GIG_01_WEBSITE_DESIGN.md:75` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1084. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/GIG_01_WEBSITE_DESIGN.md:90` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1085. **INCOME** `PRODUCTS/FIVERR_INSTANT_UPLOAD/GIG_01_WEBSITE_DESIGN.md:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1086. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:6` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1087. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:112` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1088. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:113` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1089. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:114` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1090. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:122` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1091. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:154` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1092. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:156` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1093. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:157` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1094. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:180` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1095. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:181` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1096. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:217` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1097. **INCOME** `PRODUCTS/listings/GUMROAD_GOV_CONTRACT_INTEL.md:218` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1098. **INCOME** `PRODUCTS/listings/WHOP_LISTING_2.md:27` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1099. **INCOME** `PRODUCTS/listings/WHOP_LISTING_2.md:28` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1100. **INCOME** `PRODUCTS/listings/WHOP_LISTING_2.md:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1101. **INCOME** `PRODUCTS/listings/WHOP_LISTING_3.md:24` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1102. **INCOME** `PRODUCTS/listings/WHOP_LISTING_3.md:51` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1103. **INCOME** `PRODUCTS/listings/WHOP_LISTING_5.md:16` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1104. **INCOME** `PRODUCTS/listings/WHOP_LISTING_5.md:41` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1105. **INCOME** `PRODUCTS/listings/WHOP_LISTING_1.md:23` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1106. **INCOME** `PRODUCTS/listings/WHOP_LISTING_1.md:35` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1107. **INCOME** `PRODUCTS/listings/UPWORK_GOV_CONTRACT_PROFILE.md:9` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1108. **INCOME** `PRODUCTS/listings/UPWORK_GOV_CONTRACT_PROFILE.md:117` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1109. **INCOME** `PRODUCTS/listings/UPWORK_GOV_CONTRACT_PROFILE.md:193` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1110. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_LISTINGS_COMPLETE.md:308` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1111. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_LISTINGS_COMPLETE.md:1801` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1112. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_LISTINGS_COMPLETE.md:1818` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1113. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/REDBUBBLE_UPLOAD_READY_20.md:376` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1114. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/REDBUBBLE_UPLOAD_READY_20.md:393` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1115. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_UPLOAD_READY_20.md:81` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1116. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_UPLOAD_READY_20.md:91` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1117. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_UPLOAD_READY_20.md:139` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1118. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_UPLOAD_READY_20.md:146` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1119. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_UPLOAD_READY_20.md:192` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1120. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_UPLOAD_READY_20.md:240` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1121. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_UPLOAD_READY_20.md:263` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1122. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_UPLOAD_READY_20.md:268` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1123. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ETSY_UPLOAD_READY_20.md:308` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1124. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ACCOUNT_NEEDS.md:96` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1125. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ACCOUNT_NEEDS.md:226` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1126. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ACCOUNT_NEEDS.md:227` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1127. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ACCOUNT_NEEDS.md:257` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1128. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:109` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1129. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:124` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1130. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:141` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1131. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:213` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1132. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:256` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1133. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:337` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1134. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:468` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1135. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:496` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1136. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:508` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1137. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:509` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1138. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:533` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1139. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:612` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1140. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:620` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1141. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:738` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1142. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:740` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1143. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:807` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1144. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:895` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1145. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:919` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1146. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/GUMROAD_LISTINGS_ENHANCED.md:924` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1147. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ACCOUNT_REQUIREMENTS.md:32` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1148. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ACCOUNT_REQUIREMENTS.md:97` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1149. **INCOME** `PRODUCTS/ECOM_LISTINGS_READY/ACCOUNT_REQUIREMENTS.md:196` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1150. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:41` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1151. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:134` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1152. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:169` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1153. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:481` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1154. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:489` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1155. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:661` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1156. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:834` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1157. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:848` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1158. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:858` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1159. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:875` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1160. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:903` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1161. **INCOME** `PRODUCTS/descriptions/PRODUCT_DESCRIPTIONS_20.md:929` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1162. **INCOME** `PRODUCTS/WHOP_INSTANT_UPLOAD/01_whop_listing.md:23` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1163. **INCOME** `PRODUCTS/WHOP_INSTANT_UPLOAD/01_whop_listing.md:35` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1164. **INCOME** `PRODUCTS/WHOP_INSTANT_UPLOAD/03_whop_listing.md:24` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1165. **INCOME** `PRODUCTS/WHOP_INSTANT_UPLOAD/03_whop_listing.md:51` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1166. **INCOME** `PRODUCTS/WHOP_INSTANT_UPLOAD/02_whop_listing.md:27` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1167. **INCOME** `PRODUCTS/WHOP_INSTANT_UPLOAD/02_whop_listing.md:28` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1168. **INCOME** `PRODUCTS/WHOP_INSTANT_UPLOAD/02_whop_listing.md:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1169. **INCOME** `PRODUCTS/WHOP_INSTANT_UPLOAD/05_whop_listing.md:16` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1170. **INCOME** `PRODUCTS/WHOP_INSTANT_UPLOAD/05_whop_listing.md:41` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1171. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:23` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1172. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:90` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1173. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:98` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1174. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:116` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1175. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:181` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1176. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:376` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1177. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:390` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1178. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:391` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1179. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:564` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1180. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:644` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1181. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:648` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1182. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:743` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1183. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:744` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1184. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:745` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1185. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:746` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1186. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:747` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1187. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:754` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1188. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:943` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1189. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1034` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1190. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1140` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1191. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1311` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1192. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1312` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1193. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1345` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1194. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1346` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1195. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1347` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1196. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1348` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1197. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1349` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1198. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1350` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1199. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1351` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1200. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1352` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1201. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1353` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1202. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1356` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1203. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1357` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1204. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1358` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1205. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1359` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1206. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1360` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1207. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1361` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1208. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1362` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1209. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1363` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1210. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.md:1364` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1211. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/11_cold_email_subject_lines.md:135` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1212. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/11_cold_email_subject_lines.md:147` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1213. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/11_cold_email_subject_lines.md:169` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1214. **CANSPAM** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/11_cold_email_subject_lines.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1215. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/WHOP_LISTINGS_QUICK.md:16` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1216. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:11` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1217. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:105` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1218. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:112` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1219. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:118` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1220. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:124` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1221. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:148` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1222. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:149` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1223. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:280` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1224. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:313` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1225. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:457` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1226. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:482` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1227. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:484` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1228. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:506` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1229. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:848` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1230. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/05_cold_email_playbook.md:882` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1231. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/08_sleep_youtube_starter.md:149` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1232. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/08_sleep_youtube_starter.md:386` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1233. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/12_viral_tweet_templates.md:162` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1234. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/12_viral_tweet_templates.md:210` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1235. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/12_viral_tweet_templates.md:212` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1236. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/12_viral_tweet_templates.md:265` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1237. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/04_ai_content_farm_blueprint.md:34` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1238. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/04_ai_content_farm_blueprint.md:35` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1239. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/04_ai_content_farm_blueprint.md:338` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1240. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/04_ai_content_farm_blueprint.md:343` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1241. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:34` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1242. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:45` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1243. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:60` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1244. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:94` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1245. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:97` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1246. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:100` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1247. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:108` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1248. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:118` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1249. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:120` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1250. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:138` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1251. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:140` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1252. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:170` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1253. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:210` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1254. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:220` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1255. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:254` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1256. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:271` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1257. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:273` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1258. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:275` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1259. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:277` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1260. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:283` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1261. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:289` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1262. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:320` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1263. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:330` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1264. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:332` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1265. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:338` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1266. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:354` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1267. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:394` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1268. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/09_funnel_teardown_guide.md:412` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1269. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:9` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1270. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:21` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1271. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:55` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1272. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:74` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1273. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:76` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1274. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:87` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1275. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:90` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1276. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:92` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1277. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:96` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1278. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:97` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1279. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:106` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1280. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:125` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1281. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:130` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1282. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:139` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1283. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:144` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1284. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:148` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1285. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:149` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1286. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:150` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1287. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:159` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1288. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:179` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1289. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:181` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1290. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:183` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1291. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:187` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1292. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:188` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1293. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:189` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1294. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:194` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1295. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:195` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1296. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:196` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1297. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:197` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1298. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:198` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1299. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:206` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1300. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:217` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1301. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:219` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1302. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:224` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1303. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:226` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1304. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:233` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1305. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:243` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1306. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:251` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1307. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:257` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1308. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:259` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1309. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:267` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1310. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:279` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1311. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:294` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1312. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:300` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1313. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:301` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1314. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:306` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1315. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:307` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1316. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:308` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1317. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:312` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1318. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:323` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1319. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:335` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1320. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:341` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1321. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:349` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1322. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:361` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1323. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:375` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1324. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:381` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1325. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:383` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1326. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:387` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1327. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:398` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1328. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:436` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1329. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:453` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1330. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:461` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1331. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:477` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1332. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:489` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1333. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:491` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1334. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:497` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1335. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:503` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1336. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:513` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1337. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:517` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1338. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:532` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1339. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:537` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1340. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:570` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1341. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:572` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1342. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:590` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1343. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:592` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1344. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:610` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1345. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:647` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1346. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:648` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1347. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:650` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1348. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:651` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1349. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:652` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1350. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:653` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1351. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:663` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1352. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/07_solopreneur_tech_stack.md:676` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1353. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/01_local_biz_client_system.md:502` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1354. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/01_local_biz_client_system.md:503` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1355. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/01_local_biz_client_system.md:504` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1356. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/01_local_biz_client_system.md:507` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1357. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/01_local_biz_client_system.md:510` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1358. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/01_local_biz_client_system.md:536` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1359. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/01_local_biz_client_system.md:553` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1360. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/LISTING_METADATA.md:52` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1361. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/LISTING_METADATA.md:77` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1362. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/LISTING_METADATA.md:108` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1363. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/LISTING_METADATA.md:174` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1364. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/LISTING_METADATA.md:195` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1365. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/LISTING_METADATA.md:253` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1366. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:64` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1367. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:195` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1368. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:321` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1369. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:328` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1370. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:492` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1371. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:566` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1372. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:725` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1373. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:731` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1374. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:907` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1375. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:1195` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1376. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:1447` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1377. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:1562` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1378. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:1567` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1379. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:1572` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1380. **PII** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:739` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1381. **PII** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:740` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1382. **PII** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:754` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1383. **PII** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:776` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1384. **PII** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/02_ai_automation_toolkit.md:983` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1385. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:179` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1386. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:181` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1387. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:199` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1388. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:201` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1389. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:203` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1390. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:323` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1391. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:404` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1392. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:421` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1393. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:423` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1394. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:425` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1395. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:471` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1396. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:473` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1397. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:544` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1398. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:553` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1399. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:572` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1400. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:620` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1401. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:622` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1402. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:901` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1403. **INCOME** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:920` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1404. **CANSPAM** `PRODUCTS/GUMROAD_INSTANT_UPLOAD/13_local_biz_cold_email_pack.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1405. **INCOME** `PRODUCTS/gov_contract_samples/FOIA_REQUEST_TEMPLATE.md:318` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1406. **PII** `PRODUCTS/gov_contract_samples/FOIA_REQUEST_TEMPLATE.md:230` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1407. **PII** `PRODUCTS/gov_contract_samples/FOIA_REQUEST_TEMPLATE.md:232` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1408. **PII** `PRODUCTS/gov_contract_samples/FOIA_REQUEST_TEMPLATE.md:234` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1409. **PII** `PRODUCTS/gov_contract_samples/FOIA_REQUEST_TEMPLATE.md:235` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1410. **PII** `PRODUCTS/gov_contract_samples/FOIA_REQUEST_TEMPLATE.md:236` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1411. **PII** `PRODUCTS/gov_contract_samples/FOIA_REQUEST_TEMPLATE.md:237` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1412. **PII** `PRODUCTS/gov_contract_samples/FOIA_REQUEST_TEMPLATE.md:239` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1413. **PII** `PRODUCTS/gov_contract_samples/FOIA_REQUEST_TEMPLATE.md:240` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1414. **PII** `PRODUCTS/gov_contract_samples/FOIA_REQUEST_TEMPLATE.md:241` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1415. **PII** `PRODUCTS/gov_contract_samples/SAMPLE_ANALYSIS_02_TRAIL_HARDENING.md:27` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1416. **INCOME** `PRODUCTS/gov_contract_samples/SAMPLE_ANALYSIS_01_MASS_TEXT_MESSAGING.md:154` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1417. **INCOME** `PRODUCTS/gov_contract_samples/SAMPLE_ANALYSIS_01_MASS_TEXT_MESSAGING.md:155` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1418. **PII** `PRODUCTS/gov_contract_samples/SAMPLE_ANALYSIS_01_MASS_TEXT_MESSAGING.md:25` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1419. **PII** `PRODUCTS/gov_contract_samples/SAMPLE_ANALYSIS_01_MASS_TEXT_MESSAGING.md:26` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1420. **PII** `PRODUCTS/gov_contract_samples/SAMPLE_ANALYSIS_03_SBOM_VULNERABILITY_SCANNING.md:26` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1421. **PII** `PRODUCTS/gov_contract_samples/SAMPLE_ANALYSIS_03_SBOM_VULNERABILITY_SCANNING.md:27` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1422. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md:23` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1423. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md:43` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1424. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md:141` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1425. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md:248` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1426. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md:271` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1427. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md:332` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1428. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md:407` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1429. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md:419` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1430. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md:489` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1431. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/UPWORK_PROFILES_5.md:532` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1432. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:16` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1433. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:18` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1434. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:110` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1435. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:169` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1436. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:630` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1437. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:749` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1438. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:1189` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1439. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:1238` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1440. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:1286` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1441. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:1473` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1442. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:2086` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1443. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:2148` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1444. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:2169` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1445. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:2283` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1446. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:2594` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1447. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/MULTI_PLATFORM_LISTINGS.md:2626` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1448. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:96` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1449. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:151` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1450. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:162` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1451. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:209` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1452. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:302` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1453. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:442` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1454. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:574` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1455. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:713` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1456. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:727` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1457. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:781` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1458. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:856` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1459. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:864` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1460. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:970` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1461. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:999` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1462. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:1014` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1463. **INCOME** `PRODUCTS/FREELANCE_LISTINGS_READY/FIVERR_GIGS_10.md:1288` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1464. **INCOME** `DIGITAL_PRODUCTS/SYSTEM_PRODUCTS_PACKAGE.md:95` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1465. **INCOME** `DIGITAL_PRODUCTS/SYSTEM_PRODUCTS_PACKAGE.md:151` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1466. **INCOME** `DIGITAL_PRODUCTS/SYSTEM_PRODUCTS_PACKAGE.md:156` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1467. **INCOME** `DIGITAL_PRODUCTS/SYSTEM_PRODUCTS_PACKAGE.md:164` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1468. **INCOME** `DIGITAL_PRODUCTS/SYSTEM_PRODUCTS_PACKAGE.md:386` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1469. **INCOME** `DIGITAL_PRODUCTS/SYSTEM_PRODUCTS_PACKAGE.md:533` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1470. **INCOME** `DIGITAL_PRODUCTS/SYSTEM_PRODUCTS_PACKAGE.md:712` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1471. **INCOME** `DIGITAL_PRODUCTS/SYSTEM_PRODUCTS_PACKAGE.md:720` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1472. **INCOME** `DIGITAL_PRODUCTS/PRODUCT1_GUMROAD_LISTING.md:38` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1473. **INCOME** `DIGITAL_PRODUCTS/PRODUCT1_GUMROAD_LISTING.md:51` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1474. **INCOME** `DIGITAL_PRODUCTS/PRODUCT1_GUMROAD_LISTING.md:69` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1475. **INCOME** `DIGITAL_PRODUCTS/PRODUCT1_GUMROAD_LISTING.md:134` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1476. **INCOME** `DIGITAL_PRODUCTS/PRODUCT1_GUMROAD_LISTING.md:193` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1477. **INCOME** `DIGITAL_PRODUCTS/PRODUCT1_GUMROAD_LISTING.md:213` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1478. **INCOME** `DIGITAL_PRODUCTS/PRODUCT1_GUMROAD_LISTING.md:215` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1479. **INCOME** `DIGITAL_PRODUCTS/PRODUCTS_2_3_4_QUICK_PREP.md:8` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1480. **INCOME** `DIGITAL_PRODUCTS/PRODUCTS_2_3_4_QUICK_PREP.md:77` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1481. **INCOME** `DIGITAL_PRODUCTS/PRODUCTS_2_3_4_QUICK_PREP.md:86` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1482. **INCOME** `DIGITAL_PRODUCTS/PRODUCTS_2_3_4_QUICK_PREP.md:87` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1483. **INCOME** `DIGITAL_PRODUCTS/PRODUCTS_2_3_4_QUICK_PREP.md:90` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1484. **INCOME** `DIGITAL_PRODUCTS/PRODUCTS_2_3_4_QUICK_PREP.md:196` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1485. **INCOME** `DIGITAL_PRODUCTS/PRODUCTS_2_3_4_QUICK_PREP.md:321` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1486. **INCOME** `DIGITAL_PRODUCTS/PRODUCTS_2_3_4_QUICK_PREP.md:322` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1487. **INCOME** `DIGITAL_PRODUCTS/GUMROAD_LAUNCH_EXECUTION_GUIDE.md:91` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1488. **INCOME** `DIGITAL_PRODUCTS/GUMROAD_LAUNCH_EXECUTION_GUIDE.md:97` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1489. **INCOME** `DIGITAL_PRODUCTS/GUMROAD_LAUNCH_EXECUTION_GUIDE.md:102` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1490. **INCOME** `DIGITAL_PRODUCTS/GUMROAD_LAUNCH_EXECUTION_GUIDE.md:383` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1491. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT3_GUMROAD_LISTING.md:114` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1492. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT3_GUMROAD_LISTING.md:238` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1493. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:7` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1494. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:24` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1495. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:33` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1496. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:61` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1497. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:62` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1498. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:63` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1499. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:78` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1500. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:80` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1501. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:87` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1502. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:99` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1503. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:100` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1504. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1505. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:102` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1506. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:104` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1507. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:107` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1508. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:148` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1509. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:173` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1510. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:174` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1511. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:190` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1512. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:210` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1513. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:227` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1514. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:228` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1515. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:245` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1516. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:260` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1517. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:265` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1518. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT4_GUMROAD_LISTING.md:282` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1519. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT2_GUMROAD_LISTING.md:69` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1520. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT2_GUMROAD_LISTING.md:116` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1521. **INCOME** `DIGITAL_PRODUCTS/listings/PRODUCT2_GUMROAD_LISTING.md:236` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1522. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/03_AI_AUTOMATION_BLUEPRINT.md:485` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1523. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/03_AI_AUTOMATION_BLUEPRINT.md:547` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1524. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/03_AI_AUTOMATION_BLUEPRINT.md:548` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1525. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/03_AI_AUTOMATION_BLUEPRINT.md:550` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1526. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/01_73_COLD_EMAIL_SUBJECT_LINES.md:135` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1527. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/01_73_COLD_EMAIL_SUBJECT_LINES.md:147` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1528. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/01_73_COLD_EMAIL_SUBJECT_LINES.md:169` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1529. **CANSPAM** `DIGITAL_PRODUCTS/ready_to_sell/01_73_COLD_EMAIL_SUBJECT_LINES.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1530. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1531. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:42` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1532. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:47` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1533. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:146` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1534. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:158` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1535. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:163` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1536. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:269` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1537. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:386` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1538. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:497` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1539. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:525` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1540. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:527` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1541. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:594` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1542. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:605` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1543. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:787` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1544. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:795` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1545. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:796` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1546. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:797` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1547. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:798` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1548. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:805` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1549. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:807` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1550. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:845` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1551. **CANSPAM** `DIGITAL_PRODUCTS/ready_to_sell/05_COLD_EMAIL_PLAYBOOK.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1552. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/04_SOLOPRENEUR_OPS_SYSTEM.md:193` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1553. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/04_SOLOPRENEUR_OPS_SYSTEM.md:491` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1554. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/04_SOLOPRENEUR_OPS_SYSTEM.md:630` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1555. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/04_SOLOPRENEUR_OPS_SYSTEM.md:631` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1556. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/04_SOLOPRENEUR_OPS_SYSTEM.md:632` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1557. **PII** `DIGITAL_PRODUCTS/ready_to_sell/04_SOLOPRENEUR_OPS_SYSTEM.md:209` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1558. **PII** `DIGITAL_PRODUCTS/ready_to_sell/04_SOLOPRENEUR_OPS_SYSTEM.md:210` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1559. **PII** `DIGITAL_PRODUCTS/ready_to_sell/04_SOLOPRENEUR_OPS_SYSTEM.md:211` — Exposed email in public content
   Fix: Remove or redact email from public-facing content
1560. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:11` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1561. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:13` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1562. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:27` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1563. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:45` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1564. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:46` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1565. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:108` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1566. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:114` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1567. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:119` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1568. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:122` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1569. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:137` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1570. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:142` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1571. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:154` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1572. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:169` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1573. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:342` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1574. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:394` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1575. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:400` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1576. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:406` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1577. **INCOME** `DIGITAL_PRODUCTS/ready_to_sell/02_FUNNEL_TEARDOWN_PACK.md:465` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1578. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_2_50_viral_tweet_templates.md:162` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1579. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_2_50_viral_tweet_templates.md:210` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1580. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_2_50_viral_tweet_templates.md:212` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1581. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_2_50_viral_tweet_templates.md:265` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1582. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_1_73_cold_email_subject_lines.md:135` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1583. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_1_73_cold_email_subject_lines.md:147` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1584. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_1_73_cold_email_subject_lines.md:169` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1585. **CANSPAM** `DIGITAL_PRODUCTS/micro_products/PRODUCT_1_73_cold_email_subject_lines.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1586. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:3` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1587. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:29` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1588. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:31` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1589. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:55` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1590. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:57` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1591. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:83` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1592. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:85` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1593. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:118` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1594. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:120` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1595. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:148` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1596. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:150` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1597. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:165` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1598. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:166` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1599. **INCOME** `DIGITAL_PRODUCTS/micro_products/MICRO_PRODUCT_SPECS.md:167` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1600. **INCOME** `DIGITAL_PRODUCTS/micro_products/TWEET_THREAD_micro_products.md:46` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1601. **INCOME** `DIGITAL_PRODUCTS/micro_products/TWEET_THREAD_micro_products.md:62` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1602. **INCOME** `DIGITAL_PRODUCTS/micro_products/GUMROAD_LISTINGS_MICRO_PRODUCTS.md:244` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1603. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:179` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1604. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:181` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1605. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:199` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1606. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:201` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1607. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:203` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1608. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:323` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1609. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:404` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1610. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:421` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1611. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:423` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1612. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:425` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1613. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:471` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1614. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:473` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1615. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:544` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1616. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:553` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1617. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:572` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1618. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:620` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1619. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:622` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1620. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:901` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1621. **INCOME** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:920` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1622. **CANSPAM** `DIGITAL_PRODUCTS/micro_products/PRODUCT_3_local_biz_cold_email_script_pack.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1623. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:15` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1624. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:24` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1625. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:40` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1626. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:96` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1627. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:101` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1628. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:104` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1629. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:119` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1630. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:124` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1631. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:141` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1632. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:167` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1633. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:168` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1634. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:169` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1635. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:170` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1636. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:172` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1637. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:262` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1638. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:287` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1639. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:339` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1640. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:363` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1641. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:391` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1642. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:397` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1643. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:405` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1644. **INCOME** `DIGITAL_PRODUCTS/pdfs/FUNNEL_TEARDOWN_PDF_READY.md:447` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1645. **INCOME** `EMAIL/GOV_CONTRACT_COLD_EMAIL.md:286` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1646. **INCOME** `EMAIL/GOV_CONTRACT_COLD_EMAIL.md:306` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1647. **INCOME** `EMAIL/GOV_CONTRACT_COLD_EMAIL.md:308` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1648. **CANSPAM** `EMAIL/GOV_CONTRACT_COLD_EMAIL.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1649. **INCOME** `EMAIL/GOV_TENDER_OUTREACH_EMAILS.md:14` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1650. **INCOME** `EMAIL/GOV_TENDER_OUTREACH_EMAILS.md:137` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1651. **INCOME** `EMAIL/GOV_TENDER_OUTREACH_EMAILS.md:186` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1652. **CANSPAM** `EMAIL/GOV_TENDER_OUTREACH_EMAILS.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1653. **INCOME** `EMAIL/sequence_v1.md:39` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1654. **INCOME** `EMAIL/sequence_v1.md:57` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1655. **INCOME** `EMAIL/sequence_v1.md:90` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1656. **INCOME** `EMAIL/sequence_v1.md:93` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1657. **INCOME** `EMAIL/sequence_v1.md:95` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1658. **CANSPAM** `EMAIL/sequence_v1.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1659. **CANSPAM** `EMAIL/triggering_events/glassdoor_spike_template.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1660. **CANSPAM** `EMAIL/triggering_events/office_move_template.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1661. **CANSPAM** `EMAIL/triggering_events/job_removed_template.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1662. **CANSPAM** `EMAIL/triggering_events/leadership_change_template.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1663. **CANSPAM** `EMAIL/triggering_events/competitor_layoff_template.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1664. **CANSPAM** `EMAIL/triggering_events/sec_filing_change_template.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1665. **INCOME** `EMAIL/sequences/reengagement_sequence.md:37` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1666. **INCOME** `EMAIL/sequences/reengagement_sequence.md:41` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1667. **INCOME** `EMAIL/sequences/reengagement_sequence.md:78` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1668. **INCOME** `EMAIL/sequences/reengagement_sequence.md:95` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1669. **INCOME** `EMAIL/sequences/reengagement_sequence.md:96` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1670. **INCOME** `EMAIL/sequences/reengagement_sequence.md:97` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1671. **INCOME** `EMAIL/sequences/reengagement_sequence.md:99` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1672. **INCOME** `EMAIL/sequences/reengagement_sequence.md:104` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1673. **CANSPAM** `EMAIL/sequences/reengagement_sequence.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1674. **CANSPAM** `EMAIL/sequences/README.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1675. **INCOME** `EMAIL/sequences/welcome_sequence.md:54` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1676. **INCOME** `EMAIL/sequences/welcome_sequence.md:58` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1677. **INCOME** `EMAIL/sequences/welcome_sequence.md:64` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1678. **INCOME** `EMAIL/sequences/welcome_sequence.md:70` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1679. **INCOME** `EMAIL/sequences/welcome_sequence.md:75` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1680. **INCOME** `EMAIL/sequences/welcome_sequence.md:157` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1681. **CANSPAM** `EMAIL/sequences/welcome_sequence.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1682. **INCOME** `EMAIL/sequences/launch_sequence.md:85` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1683. **INCOME** `EMAIL/sequences/launch_sequence.md:166` — Income claim without disclaimer
   Fix: Add 'Results may vary. Not a guarantee of income.' near this claim
1684. **FAKE_PROOF** `EMAIL/sequences/launch_sequence.md:249` — Potentially unverifiable social proof claim
   Fix: Replace with verifiable claim or remove specific numbers
1685. **CANSPAM** `EMAIL/sequences/launch_sequence.md:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1686. **CANSPAM** `EMAIL/ecom_outreach/tech_stack_template.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements
1687. **CANSPAM** `EMAIL/ecom_outreach/growth_offer_template.txt:0` — Email may be missing physical address
   Fix: Add physical business address per CAN-SPAM requirements

## INFO (review optional)

- `CONTENT/social/reddit/REDDIT_POSTING_SCHEDULE.md:381` — Language that may trigger platform TOS enforcement
- `CONTENT/social/reddit/REDDIT_POSTS_30.md:56` — Language that may trigger platform TOS enforcement
- `AUTOMATIONS/content_posting/printmaxxer_tweets_50.csv:13` — Language that may trigger platform TOS enforcement
- `PRODUCTS/GUMROAD_INSTANT_UPLOAD/12_viral_tweet_templates.md:132` — Language that may trigger platform TOS enforcement
- `DIGITAL_PRODUCTS/micro_products/PRODUCT_2_50_viral_tweet_templates.md:132` — Language that may trigger platform TOS enforcement
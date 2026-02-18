# Thread: What Running AI Agents Overnight Actually Looks Like

## Tweet 1
I run AI agents overnight to generate content while I sleep.

Sounds fancy. Reality is messier.

Here's what actually happens when you automate content generation:

## Tweet 2
Night 1: Disaster

Prompt: "Generate 50 blog post ideas"

Woke up to 50 ideas like "10 Ways to Use AI" and "AI Tips for Beginners."

All generic. All useless. Learned: vague prompts get vague outputs at scale.

## Tweet 3
Night 2: Better, still broken

Added constraints: "Generate 50 blog post ideas. Include specific tools and numbers."

Woke up to better titles. But 12 of them were duplicates with different wording.

Learned: AI doesn't check its own output for redundancy.

## Tweet 4
Night 3: Quality filter needed

Added a second agent to score each idea on originality (1-10).

Only kept ideas scoring 7+. Got 23 ideas from 50 generations.

Math worked: 23 good ideas vs 0 good ideas on night 1.

## Tweet 5
Night 4: Cost explosion

Ran agents on GPT-4. Woke up to $47 in API costs for 50 blog posts.

Switched to Claude Haiku for bulk generation. Same output quality, $4 instead.

Learned: model selection matters at scale. Sonnet for quality checks, Haiku for bulk.

## Tweet 6
Night 5: The working system

Agent 1: Generate 100 ideas (Haiku, cheap)
Agent 2: Score each 1-10 (Haiku, fast)
Agent 3: Expand top 20 to outlines (Sonnet, quality)
Agent 4: Write 5 full posts from best outlines (Sonnet)

Total cost: $8 per night
Output: 5 usable blog posts

## Tweet 7
Reality check:

I still edit every post for 30 minutes.
About 1 in 5 posts is unusable.
I spend 2 hours per week fixing broken agents.

But I get 20 posts per week vs 2 posts when I wrote everything manually.

Agents don't replace work. They shift it from creation to editing.

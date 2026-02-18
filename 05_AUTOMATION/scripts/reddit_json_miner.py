#!/usr/bin/env python3
"""
Reddit JSON Miner - Extract Pain Points & Startup Ideas

The Reddit JSON Hack:
- Add /.json to any Reddit URL
- Get full thread with all comments in structured format
- No API key needed, no scraping tools
- Pass through Claude to extract pain points

Usage:
    python3 reddit_json_miner.py --subreddit Entrepreneur --limit 50
    python3 reddit_json_miner.py --url "https://reddit.com/r/SaaS/comments/xyz"
    python3 reddit_json_miner.py --batch  # Process all target subreddits
"""

import requests
import json
import csv
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

PROJECT_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt")
LEDGER_DIR = PROJECT_DIR / "LEDGER"
OUTPUT_DIR = PROJECT_DIR / "RESEARCH" / "reddit_insights"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Target subreddits (from user's list)
TARGET_SUBREDDITS = [
    ("InternetIsBeautiful", 17000000),
    ("Entrepreneur", 4800000),
    ("productivity", 4000000),
    ("business", 2500000),
    ("smallbusiness", 2200000),
    ("startups", 2000000),
    ("passive_income", 1000000),
    ("EntrepreneurRideAlong", 593000),
    ("SideProject", 430000),
    ("Business_Ideas", 359000),
    ("SaaS", 341000),
    ("startup", 267000),
    ("Startup_Ideas", 241000),
    ("thesidehustle", 184000),
    ("juststart", 170000),
    ("MicroSaas", 155000),
    ("ycombinator", 132000),
    ("Entrepreneurs", 110000),
    ("indiehackers", 91000),
    ("GrowthHacking", 77000),
    ("AppIdeas", 74000),
    ("growmybusiness", 63000),
    ("buildinpublic", 55000),
    ("micro_saas", 52000),
    ("Solopreneur", 43000),
    ("vibecoding", 35000),
    ("startup_resources", 33000),
    ("indiebiz", 29000),
    ("AlphaandBetaUsers", 21000),
    ("scaleinpublic", 11000),
]

class RedditJSONMiner:
    """Mine Reddit for pain points and startup ideas using JSON hack"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def get_subreddit_hot(self, subreddit: str, limit: int = 25) -> List[Dict]:
        """Get hot posts from subreddit using JSON hack"""
        url = f"https://reddit.com/r/{subreddit}/hot.json?limit={limit}"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()

            posts = []
            for post in data['data']['children']:
                post_data = post['data']
                posts.append({
                    'id': post_data.get('id'),
                    'title': post_data.get('title'),
                    'selftext': post_data.get('selftext', ''),
                    'score': post_data.get('score'),
                    'num_comments': post_data.get('num_comments'),
                    'url': f"https://reddit.com{post_data.get('permalink')}",
                    'created_utc': post_data.get('created_utc'),
                })

            return posts
        except Exception as e:
            print(f"Error fetching {subreddit}: {e}")
            return []

    def get_post_comments(self, post_url: str) -> Dict:
        """Get all comments from a post using JSON hack"""
        json_url = post_url.rstrip('/') + '.json'

        try:
            response = self.session.get(json_url)
            response.raise_for_status()
            data = response.json()

            # First element is post data, second is comments
            post = data[0]['data']['children'][0]['data']
            comments = self._extract_comments(data[1]['data']['children'])

            return {
                'title': post.get('title'),
                'selftext': post.get('selftext', ''),
                'score': post.get('score'),
                'num_comments': post.get('num_comments'),
                'comments': comments
            }
        except Exception as e:
            print(f"Error fetching comments from {post_url}: {e}")
            return {}

    def _extract_comments(self, comment_tree: List, depth: int = 0) -> List[Dict]:
        """Recursively extract nested comments"""
        comments = []

        for item in comment_tree:
            if item['kind'] == 't1':  # Comment
                comment = item['data']

                # Extract pain point keywords
                body = comment.get('body', '').lower()
                is_pain_point = any(keyword in body for keyword in [
                    'i wish', 'i\'d pay', 'why doesn\'t', 'frustrated',
                    'annoying', 'need', 'want', 'looking for', 'trying to find'
                ])

                comments.append({
                    'body': comment.get('body', ''),
                    'score': comment.get('score'),
                    'depth': depth,
                    'is_pain_point': is_pain_point,
                })

                # Get nested replies
                if 'replies' in comment and comment['replies']:
                    nested = self._extract_comments(
                        comment['replies']['data']['children'],
                        depth + 1
                    )
                    comments.extend(nested)

        return comments

    def extract_pain_points(self, subreddit: str, limit: int = 50) -> List[Dict]:
        """Extract pain points from subreddit"""
        print(f"Mining r/{subreddit} for pain points...")

        # Get hot posts
        posts = self.get_subreddit_hot(subreddit, limit)

        pain_points = []

        for i, post in enumerate(posts):
            print(f"  Analyzing post {i+1}/{len(posts)}: {post['title'][:50]}...")

            # Get comments
            full_post = self.get_post_comments(post['url'])

            if not full_post:
                continue

            # Extract pain points from comments
            for comment in full_post.get('comments', []):
                if comment['is_pain_point']:
                    pain_points.append({
                        'subreddit': subreddit,
                        'post_title': post['title'],
                        'post_url': post['url'],
                        'comment': comment['body'],
                        'score': comment['score'],
                        'extracted_at': datetime.now().isoformat()
                    })

            # Rate limit
            time.sleep(2)

        return pain_points

    def save_pain_points(self, pain_points: List[Dict], filename: str = None):
        """Save pain points to CSV"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"pain_points_{timestamp}.csv"

        filepath = OUTPUT_DIR / filename

        if not pain_points:
            print("No pain points found")
            return

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=pain_points[0].keys())
            writer.writeheader()
            writer.writerows(pain_points)

        print(f"\nSaved {len(pain_points)} pain points to {filepath}")

    def batch_mine_all_subreddits(self, limit_per_sub: int = 25):
        """Mine all target subreddits"""
        all_pain_points = []

        for subreddit, subscribers in TARGET_SUBREDDITS:
            print(f"\n{'='*60}")
            print(f"r/{subreddit} ({subscribers:,} subscribers)")
            print('='*60)

            pain_points = self.extract_pain_points(subreddit, limit_per_sub)
            all_pain_points.extend(pain_points)

            # Rate limit between subreddits
            time.sleep(5)

        # Save all
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.save_pain_points(all_pain_points, f"all_subreddits_{timestamp}.csv")

        # Generate summary
        self._generate_summary(all_pain_points)

    def _generate_summary(self, pain_points: List[Dict]):
        """Generate summary of findings"""
        summary_file = OUTPUT_DIR / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        # Count by subreddit
        by_subreddit = {}
        for pp in pain_points:
            sub = pp['subreddit']
            by_subreddit[sub] = by_subreddit.get(sub, 0) + 1

        # Find common themes
        all_text = ' '.join([pp['comment'].lower() for pp in pain_points])

        summary = f"""# Reddit Pain Point Mining Summary

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Total Pain Points:** {len(pain_points)}

## By Subreddit

"""
        for sub, count in sorted(by_subreddit.items(), key=lambda x: x[1], reverse=True):
            summary += f"- r/{sub}: {count} pain points\n"

        summary += f"""

## Next Steps

1. Pass pain points through Claude for analysis
2. Identify recurring patterns (same complaint 10+ times)
3. Look for validation signals:
   - "I wish someone would build..."
   - "I'd pay for..."
   - "Why doesn't X exist?"
   - "Frustrated with..."
4. Prioritize by frequency + intensity
5. Build MVP for highest-signal opportunities

## Files Generated

- Full data: Check RESEARCH/reddit_insights/ directory
- Pain points CSV ready for analysis

**The internet is telling you what to build. You just have to listen.**
"""

        with open(summary_file, 'w') as f:
            f.write(summary)

        print(f"\nSummary saved to {summary_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Reddit JSON Pain Point Miner')
    parser.add_argument('--subreddit', help='Single subreddit to mine')
    parser.add_argument('--url', help='Specific post URL to analyze')
    parser.add_argument('--batch', action='store_true', help='Mine all target subreddits')
    parser.add_argument('--limit', type=int, default=25, help='Posts per subreddit')

    args = parser.parse_args()

    miner = RedditJSONMiner()

    if args.batch:
        print("Mining all target subreddits...")
        miner.batch_mine_all_subreddits(args.limit)

    elif args.subreddit:
        pain_points = miner.extract_pain_points(args.subreddit, args.limit)
        miner.save_pain_points(pain_points)

    elif args.url:
        post_data = miner.get_post_comments(args.url)
        print(json.dumps(post_data, indent=2))

    else:
        print("Please specify --subreddit, --url, or --batch")
        parser.print_help()


if __name__ == "__main__":
    main()

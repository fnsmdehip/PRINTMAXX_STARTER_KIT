# AI Automation Starter Kit

## 10 scripts. 5 recipes. 1 overnight loop. run them tonight.

---

## Part 1: Environment Setup

before running anything, set up your environment once. takes 10 minutes.

### prerequisites

- Python 3.10+ (`python3 --version` to check)
- pip (`pip3 --version` to check)
- a text editor (VS Code, Cursor, whatever)
- terminal access (Terminal on macOS, Command Prompt or WSL on Windows)

### virtual environment setup

```bash
# create a project folder
mkdir my-automations && cd my-automations

# create virtual environment
python3 -m venv venv

# activate it
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# install common dependencies
pip3 install requests beautifulsoup4 schedule python-dotenv
```

### environment variables

create a `.env` file in your project root:

```
# API keys (add as needed)
ANTHROPIC_API_KEY=sk-ant-your-key-here
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ALERT_EMAIL=alerts@yourdomain.com

# paths
DATA_DIR=./data
LOGS_DIR=./logs
STATE_DIR=./state
```

load them in every script:

```python
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
```

### folder structure

```
my-automations/
  .env
  scripts/
    web_scraper.py
    content_scheduler.py
    lead_processor.py
    file_monitor.py
    api_poller.py
    data_cleaner.py
    csv_aggregator.py
    alert_sender.py
    report_generator.py
    backup_automator.py
  data/          # scraped data, CSVs, etc.
  logs/          # execution logs
  state/         # state files for persistence
  prompts/       # prompt templates for Claude
```

---

## Part 2: The 10 Scripts

### Script 1: Web Scraper

scrapes a list of URLs and extracts text content. useful for monitoring competitors, scraping job boards, or collecting research.

```python
#!/usr/bin/env python3
"""web_scraper.py - scrape URLs and save content to files"""

import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")
os.makedirs(DATA_DIR, exist_ok=True)

# configure your targets
TARGETS = [
    {"name": "competitor-pricing", "url": "https://example.com/pricing", "selector": ".pricing-card"},
    {"name": "job-board", "url": "https://example.com/jobs", "selector": ".job-listing"},
    # add more targets here
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

def scrape_target(target):
    """scrape a single target and return extracted text"""
    try:
        resp = requests.get(target["url"], headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        if target.get("selector"):
            elements = soup.select(target["selector"])
            content = [el.get_text(strip=True) for el in elements]
        else:
            # fallback: get all paragraph text
            content = [p.get_text(strip=True) for p in soup.find_all("p")]

        return {
            "name": target["name"],
            "url": target["url"],
            "scraped_at": datetime.now().isoformat(),
            "content": content,
            "content_count": len(content)
        }
    except Exception as e:
        return {
            "name": target["name"],
            "url": target["url"],
            "error": str(e),
            "scraped_at": datetime.now().isoformat()
        }

def detect_changes(name, new_content):
    """compare with previous scrape, return True if changed"""
    state_file = os.path.join(DATA_DIR, f"{name}_last.json")
    changed = False

    if os.path.exists(state_file):
        with open(state_file) as f:
            old = json.load(f)
        if old.get("content") != new_content.get("content"):
            changed = True
            print(f"  CHANGE DETECTED in {name}")
    else:
        changed = True  # first run counts as "new"

    # save current state
    with open(state_file, "w") as f:
        json.dump(new_content, f, indent=2)

    return changed

def main():
    print(f"scraping {len(TARGETS)} targets at {datetime.now().isoformat()}")
    results = []

    for target in TARGETS:
        print(f"  scraping: {target['name']}")
        result = scrape_target(target)

        if "error" not in result:
            changed = detect_changes(target["name"], result)
            result["changed"] = changed

        results.append(result)

    # save full results
    output_file = os.path.join(DATA_DIR, f"scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    # summary
    errors = [r for r in results if "error" in r]
    changes = [r for r in results if r.get("changed")]
    print(f"\ndone. {len(results)} scraped, {len(changes)} changed, {len(errors)} errors.")

    if changes:
        print("changes in:", [r["name"] for r in changes])

if __name__ == "__main__":
    main()
```

---

### Script 2: Content Scheduler

reads content from a folder and posts to a scheduling queue with timestamps.

```python
#!/usr/bin/env python3
"""content_scheduler.py - queue content for posting at scheduled times"""

import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")
CONTENT_DIR = os.path.join(DATA_DIR, "content_queue")
SCHEDULE_FILE = os.path.join(DATA_DIR, "schedule.json")

os.makedirs(CONTENT_DIR, exist_ok=True)

# posting schedule: day_of_week -> list of times (24h format)
POSTING_SCHEDULE = {
    "monday":    ["09:00", "13:00", "17:30"],
    "tuesday":   ["09:00", "13:00", "17:30"],
    "wednesday": ["09:00", "13:00", "17:30"],
    "thursday":  ["09:00", "13:00", "17:30"],
    "friday":    ["09:00", "13:00"],
    "saturday":  ["10:00"],
    "sunday":    ["10:00"],
}

def load_queue():
    """load all .txt files from content queue"""
    posts = []
    for f in sorted(os.listdir(CONTENT_DIR)):
        if f.endswith(".txt"):
            filepath = os.path.join(CONTENT_DIR, f)
            with open(filepath) as fh:
                content = fh.read().strip()
            posts.append({"file": f, "content": content, "path": filepath})
    return posts

def generate_schedule(posts, start_date=None):
    """assign each post to the next available time slot"""
    if start_date is None:
        start_date = datetime.now()

    schedule = []
    current_date = start_date
    post_index = 0

    while post_index < len(posts):
        day_name = current_date.strftime("%A").lower()
        times = POSTING_SCHEDULE.get(day_name, [])

        for time_str in times:
            if post_index >= len(posts):
                break

            hour, minute = map(int, time_str.split(":"))
            post_time = current_date.replace(hour=hour, minute=minute, second=0)

            # skip times in the past
            if post_time <= datetime.now():
                continue

            schedule.append({
                "post_time": post_time.isoformat(),
                "content": posts[post_index]["content"],
                "source_file": posts[post_index]["file"],
                "status": "scheduled"
            })
            post_index += 1

        current_date += timedelta(days=1)

    return schedule

def main():
    posts = load_queue()
    print(f"found {len(posts)} posts in queue")

    if not posts:
        print("no content to schedule. add .txt files to", CONTENT_DIR)
        return

    schedule = generate_schedule(posts)

    with open(SCHEDULE_FILE, "w") as f:
        json.dump(schedule, f, indent=2, default=str)

    print(f"scheduled {len(schedule)} posts")
    for item in schedule[:5]:  # preview first 5
        print(f"  {item['post_time']} -> {item['content'][:60]}...")

    if len(schedule) > 5:
        print(f"  ... and {len(schedule) - 5} more")

if __name__ == "__main__":
    main()
```

---

### Script 3: Lead Processor

takes raw lead data (CSV), cleans it, deduplicates, and scores leads based on criteria you define.

```python
#!/usr/bin/env python3
"""lead_processor.py - clean, deduplicate, and score leads from CSV"""

import csv
import os
import re
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")

def clean_email(email):
    """normalize and validate email"""
    if not email:
        return None
    email = email.strip().lower()
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return email
    return None

def clean_name(name):
    """normalize name"""
    if not name:
        return ""
    return " ".join(name.strip().split()).title()

def score_lead(lead):
    """score a lead 0-100 based on completeness and quality signals"""
    score = 0

    # has valid email: +30
    if lead.get("email"):
        score += 30

    # has company name: +15
    if lead.get("company"):
        score += 15

    # has phone: +10
    if lead.get("phone"):
        score += 10

    # has website: +15
    if lead.get("website"):
        score += 15
        # bonus for https
        if lead["website"].startswith("https"):
            score += 5

    # has title/role: +10
    if lead.get("title"):
        score += 10
        # bonus for decision-maker titles
        dm_titles = ["ceo", "founder", "owner", "director", "head", "vp", "president"]
        if any(t in lead["title"].lower() for t in dm_titles):
            score += 15

    return min(score, 100)

def process_leads(input_file, output_file):
    """main processing pipeline"""
    leads = []
    seen_emails = set()
    stats = Counter()

    with open(input_file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stats["total"] += 1

            # clean fields
            email = clean_email(row.get("email", ""))
            if not email:
                stats["invalid_email"] += 1
                continue

            # deduplicate
            if email in seen_emails:
                stats["duplicate"] += 1
                continue
            seen_emails.add(email)

            lead = {
                "name": clean_name(row.get("name", "")),
                "email": email,
                "company": row.get("company", "").strip(),
                "title": row.get("title", "").strip(),
                "phone": row.get("phone", "").strip(),
                "website": row.get("website", "").strip(),
                "source": row.get("source", "manual"),
            }

            lead["score"] = score_lead(lead)
            lead["processed_at"] = datetime.now().isoformat()
            leads.append(lead)
            stats["valid"] += 1

    # sort by score descending
    leads.sort(key=lambda x: x["score"], reverse=True)

    # write output
    if leads:
        fieldnames = leads[0].keys()
        with open(output_file, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(leads)

    return leads, stats

def main():
    input_file = os.path.join(DATA_DIR, "raw_leads.csv")
    output_file = os.path.join(DATA_DIR, f"processed_leads_{datetime.now().strftime('%Y%m%d')}.csv")

    if not os.path.exists(input_file):
        print(f"no input file found at {input_file}")
        print("create a CSV with columns: name, email, company, title, phone, website, source")
        return

    leads, stats = process_leads(input_file, output_file)

    print(f"lead processing complete:")
    print(f"  total rows: {stats['total']}")
    print(f"  valid leads: {stats['valid']}")
    print(f"  invalid emails: {stats['invalid_email']}")
    print(f"  duplicates removed: {stats['duplicate']}")
    print(f"  output: {output_file}")

    if leads:
        print(f"\ntop 5 leads by score:")
        for lead in leads[:5]:
            print(f"  [{lead['score']}] {lead['name']} - {lead['company']} ({lead['email']})")

if __name__ == "__main__":
    main()
```

---

### Script 4: File Monitor

watches a directory for new or changed files and triggers actions.

```python
#!/usr/bin/env python3
"""file_monitor.py - watch a directory and trigger actions on changes"""

import os
import json
import time
import hashlib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
STATE_DIR = os.getenv("STATE_DIR", "./state")
os.makedirs(STATE_DIR, exist_ok=True)

# configure what to watch
WATCH_DIRS = [
    {"path": "./data", "extensions": [".csv", ".json"], "action": "log"},
    {"path": "./data/content_queue", "extensions": [".txt"], "action": "count"},
    # add more watch targets here
]

STATE_FILE = os.path.join(STATE_DIR, "file_monitor_state.json")

def file_hash(filepath):
    """get md5 hash of file content"""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def scan_directory(watch_config):
    """scan a directory and return file states"""
    path = watch_config["path"]
    extensions = watch_config.get("extensions", [])

    files = {}
    if not os.path.exists(path):
        return files

    for f in os.listdir(path):
        filepath = os.path.join(path, f)
        if not os.path.isfile(filepath):
            continue
        if extensions and not any(f.endswith(ext) for ext in extensions):
            continue

        files[filepath] = {
            "size": os.path.getsize(filepath),
            "modified": os.path.getmtime(filepath),
            "hash": file_hash(filepath)
        }

    return files

def load_state():
    """load previous state"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}

def save_state(state):
    """save current state"""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def handle_action(action, event_type, filepath):
    """execute action based on change type"""
    timestamp = datetime.now().isoformat()

    if action == "log":
        log_line = f"[{timestamp}] {event_type}: {filepath}\n"
        log_file = os.path.join(STATE_DIR, "file_changes.log")
        with open(log_file, "a") as f:
            f.write(log_line)
        print(f"  logged: {event_type} -> {filepath}")

    elif action == "count":
        print(f"  {event_type}: {filepath}")

    # add custom actions here:
    # elif action == "notify":
    #     send_alert(f"{event_type}: {filepath}")

def main():
    print(f"file monitor running at {datetime.now().isoformat()}")
    old_state = load_state()
    new_state = {}
    changes = {"new": [], "modified": [], "deleted": []}

    for watch in WATCH_DIRS:
        path = watch["path"]
        action = watch.get("action", "log")
        current_files = scan_directory(watch)

        old_files = old_state.get(path, {})

        # detect new and modified files
        for filepath, info in current_files.items():
            if filepath not in old_files:
                changes["new"].append(filepath)
                handle_action(action, "NEW", filepath)
            elif info["hash"] != old_files[filepath].get("hash"):
                changes["modified"].append(filepath)
                handle_action(action, "MODIFIED", filepath)

        # detect deleted files
        for filepath in old_files:
            if filepath not in current_files:
                changes["deleted"].append(filepath)
                handle_action(action, "DELETED", filepath)

        new_state[path] = current_files

    save_state(new_state)

    total = len(changes["new"]) + len(changes["modified"]) + len(changes["deleted"])
    print(f"\nsummary: {total} changes ({len(changes['new'])} new, {len(changes['modified'])} modified, {len(changes['deleted'])} deleted)")

if __name__ == "__main__":
    main()
```

---

### Script 5: API Poller

polls APIs at intervals and saves responses. useful for tracking prices, stock data, or any data that updates.

```python
#!/usr/bin/env python3
"""api_poller.py - poll APIs and save responses with change detection"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")
STATE_DIR = os.getenv("STATE_DIR", "./state")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STATE_DIR, exist_ok=True)

# configure your API endpoints
ENDPOINTS = [
    {
        "name": "bitcoin-price",
        "url": "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
        "method": "GET",
        "headers": {},
        "extract": lambda r: r.json().get("bitcoin", {}).get("usd"),
    },
    {
        "name": "github-stars",
        "url": "https://api.github.com/repos/anthropics/claude-code",
        "method": "GET",
        "headers": {"Accept": "application/vnd.github.v3+json"},
        "extract": lambda r: r.json().get("stargazers_count"),
    },
    # add your own endpoints here
]

def poll_endpoint(endpoint):
    """poll a single endpoint and return extracted data"""
    try:
        if endpoint["method"] == "GET":
            resp = requests.get(endpoint["url"], headers=endpoint.get("headers", {}), timeout=10)
        elif endpoint["method"] == "POST":
            resp = requests.post(endpoint["url"], headers=endpoint.get("headers", {}),
                               json=endpoint.get("body", {}), timeout=10)

        resp.raise_for_status()

        extractor = endpoint.get("extract")
        value = extractor(resp) if extractor else resp.json()

        return {
            "name": endpoint["name"],
            "value": value,
            "status": resp.status_code,
            "polled_at": datetime.now().isoformat(),
        }
    except Exception as e:
        return {
            "name": endpoint["name"],
            "error": str(e),
            "polled_at": datetime.now().isoformat(),
        }

def check_threshold(name, value):
    """check if value crosses a threshold (customize per endpoint)"""
    # example: alert if bitcoin drops below 50000
    thresholds = {
        "bitcoin-price": {"low": 50000, "high": 100000},
    }

    if name in thresholds and isinstance(value, (int, float)):
        t = thresholds[name]
        if value < t.get("low", float("-inf")):
            return f"ALERT: {name} is {value}, below threshold {t['low']}"
        if value > t.get("high", float("inf")):
            return f"ALERT: {name} is {value}, above threshold {t['high']}"
    return None

def main():
    print(f"polling {len(ENDPOINTS)} endpoints at {datetime.now().isoformat()}")
    results = []
    alerts = []

    for endpoint in ENDPOINTS:
        result = poll_endpoint(endpoint)
        results.append(result)

        if "error" in result:
            print(f"  ERROR {result['name']}: {result['error']}")
        else:
            print(f"  {result['name']}: {result['value']}")
            alert = check_threshold(result["name"], result["value"])
            if alert:
                alerts.append(alert)
                print(f"  {alert}")

    # append to history
    history_file = os.path.join(DATA_DIR, "api_poll_history.jsonl")
    with open(history_file, "a") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")

    if alerts:
        print(f"\n{len(alerts)} alerts triggered")

if __name__ == "__main__":
    main()
```

---

### Script 6: Data Cleaner

cleans messy CSV data: trims whitespace, normalizes formats, removes empty rows, standardizes dates.

```python
#!/usr/bin/env python3
"""data_cleaner.py - clean and normalize CSV data"""

import csv
import os
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")

def clean_value(value):
    """basic value cleaning"""
    if value is None:
        return ""
    value = str(value).strip()
    # remove multiple spaces
    value = re.sub(r'\s+', ' ', value)
    # remove zero-width characters
    value = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', value)
    return value

def normalize_phone(phone):
    """normalize phone to digits only with country code"""
    digits = re.sub(r'[^\d+]', '', phone)
    if len(digits) == 10:
        digits = "+1" + digits
    return digits if len(digits) >= 10 else ""

def normalize_url(url):
    """ensure URL has protocol"""
    url = url.strip().lower()
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url

def clean_csv(input_file, output_file):
    """clean a CSV file"""
    clean_rows = []
    removed = 0

    with open(input_file, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            # clean all values
            cleaned = {k: clean_value(v) for k, v in row.items()}

            # skip completely empty rows
            if not any(cleaned.values()):
                removed += 1
                continue

            # normalize specific fields if they exist
            if "phone" in cleaned:
                cleaned["phone"] = normalize_phone(cleaned["phone"])
            if "website" in cleaned:
                cleaned["website"] = normalize_url(cleaned["website"])
            if "email" in cleaned:
                cleaned["email"] = cleaned["email"].lower()

            clean_rows.append(cleaned)

    with open(output_file, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clean_rows)

    return len(clean_rows), removed

def main():
    input_file = os.path.join(DATA_DIR, "messy_data.csv")
    output_file = os.path.join(DATA_DIR, "clean_data.csv")

    if not os.path.exists(input_file):
        print(f"no input file at {input_file}")
        return

    kept, removed = clean_csv(input_file, output_file)
    print(f"cleaned: {kept} rows kept, {removed} empty rows removed")
    print(f"output: {output_file}")

if __name__ == "__main__":
    main()
```

---

### Script 7: CSV Aggregator

combines multiple CSV files into one master file with deduplication.

```python
#!/usr/bin/env python3
"""csv_aggregator.py - combine multiple CSVs into one master file"""

import csv
import os
import glob
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")

def aggregate_csvs(input_pattern, output_file, dedup_key=None):
    """combine all matching CSVs into one file"""
    files = sorted(glob.glob(input_pattern))

    if not files:
        print(f"no files matching {input_pattern}")
        return 0, 0

    all_rows = []
    all_fieldnames = set()
    seen_keys = set()
    dupes = 0

    for filepath in files:
        with open(filepath, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            all_fieldnames.update(reader.fieldnames or [])

            for row in reader:
                # dedup check
                if dedup_key and row.get(dedup_key):
                    key = row[dedup_key].strip().lower()
                    if key in seen_keys:
                        dupes += 1
                        continue
                    seen_keys.add(key)

                row["_source_file"] = os.path.basename(filepath)
                row["_aggregated_at"] = datetime.now().isoformat()
                all_rows.append(row)

    # add meta fields
    all_fieldnames.update(["_source_file", "_aggregated_at"])
    fieldnames = sorted(all_fieldnames)

    with open(output_file, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(all_rows)

    return len(all_rows), dupes

def main():
    pattern = os.path.join(DATA_DIR, "processed_leads_*.csv")
    output = os.path.join(DATA_DIR, "master_leads.csv")

    rows, dupes = aggregate_csvs(pattern, output, dedup_key="email")
    print(f"aggregated: {rows} rows from matching files, {dupes} duplicates removed")
    print(f"output: {output}")

if __name__ == "__main__":
    main()
```

---

### Script 8: Alert Sender

sends email alerts when triggered by other scripts or conditions.

```python
#!/usr/bin/env python3
"""alert_sender.py - send email alerts via SMTP"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ALERT_EMAIL = os.getenv("ALERT_EMAIL", SMTP_EMAIL)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

def send_alert(subject, body, to_email=None):
    """send an email alert"""
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        print(f"ALERT (email not configured): {subject}")
        print(f"  {body}")
        # fallback: write to file
        log_file = os.path.join(os.getenv("STATE_DIR", "./state"), "alerts.log")
        with open(log_file, "a") as f:
            f.write(f"[{datetime.now().isoformat()}] {subject}: {body}\n")
        return False

    to_email = to_email or ALERT_EMAIL

    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg["Subject"] = f"[AUTOMATION ALERT] {subject}"

    body_with_meta = f"{body}\n\n---\nSent at: {datetime.now().isoformat()}\nFrom: automation alert system"
    msg.attach(MIMEText(body_with_meta, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"alert sent: {subject} -> {to_email}")
        return True
    except Exception as e:
        print(f"failed to send alert: {e}")
        return False

def check_and_alert():
    """example: check conditions and send alerts"""
    state_dir = os.getenv("STATE_DIR", "./state")
    alerts_needed = []

    # check for change detection alerts
    change_log = os.path.join(state_dir, "file_changes.log")
    if os.path.exists(change_log):
        with open(change_log) as f:
            lines = f.readlines()
        recent = [l for l in lines if l.strip()][-5:]  # last 5 changes
        if recent:
            alerts_needed.append({
                "subject": f"{len(recent)} recent file changes",
                "body": "".join(recent)
            })

    for alert in alerts_needed:
        send_alert(alert["subject"], alert["body"])

if __name__ == "__main__":
    check_and_alert()
```

---

### Script 9: Report Generator

generates a daily summary report from all your automation data.

```python
#!/usr/bin/env python3
"""report_generator.py - generate daily summary from automation data"""

import os
import json
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")
STATE_DIR = os.getenv("STATE_DIR", "./state")

def count_csv_rows(filepath):
    """count rows in a CSV file"""
    if not os.path.exists(filepath):
        return 0
    with open(filepath) as f:
        return sum(1 for _ in csv.reader(f)) - 1  # subtract header

def get_latest_poll_data():
    """get most recent API poll results"""
    history_file = os.path.join(DATA_DIR, "api_poll_history.jsonl")
    if not os.path.exists(history_file):
        return []

    latest = {}
    with open(history_file) as f:
        for line in f:
            if line.strip():
                entry = json.loads(line)
                latest[entry["name"]] = entry
    return list(latest.values())

def generate_report():
    """generate daily summary report"""
    now = datetime.now()
    report_lines = [
        f"# daily automation report",
        f"## {now.strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    # lead stats
    master_leads = os.path.join(DATA_DIR, "master_leads.csv")
    lead_count = count_csv_rows(master_leads)
    report_lines.append(f"### leads")
    report_lines.append(f"- total leads in master file: {lead_count}")
    report_lines.append("")

    # API poll data
    poll_data = get_latest_poll_data()
    if poll_data:
        report_lines.append("### api data")
        for entry in poll_data:
            if "error" in entry:
                report_lines.append(f"- {entry['name']}: ERROR - {entry['error']}")
            else:
                report_lines.append(f"- {entry['name']}: {entry['value']} (as of {entry['polled_at'][:16]})")
        report_lines.append("")

    # file changes
    change_log = os.path.join(STATE_DIR, "file_changes.log")
    if os.path.exists(change_log):
        with open(change_log) as f:
            changes = f.readlines()
        today_changes = [c for c in changes if now.strftime("%Y-%m-%d") in c]
        report_lines.append(f"### file changes today: {len(today_changes)}")
        for change in today_changes[-5:]:
            report_lines.append(f"- {change.strip()}")
        report_lines.append("")

    # content queue
    content_dir = os.path.join(DATA_DIR, "content_queue")
    if os.path.exists(content_dir):
        queued = len([f for f in os.listdir(content_dir) if f.endswith(".txt")])
        report_lines.append(f"### content queue: {queued} posts waiting")
        report_lines.append("")

    # alerts
    alert_log = os.path.join(STATE_DIR, "alerts.log")
    if os.path.exists(alert_log):
        with open(alert_log) as f:
            alerts = f.readlines()
        today_alerts = [a for a in alerts if now.strftime("%Y-%m-%d") in a]
        report_lines.append(f"### alerts today: {len(today_alerts)}")
        for alert in today_alerts:
            report_lines.append(f"- {alert.strip()}")
        report_lines.append("")

    report = "\n".join(report_lines)

    # save report
    report_file = os.path.join(DATA_DIR, f"report_{now.strftime('%Y%m%d')}.md")
    with open(report_file, "w") as f:
        f.write(report)

    print(report)
    print(f"\nreport saved to {report_file}")
    return report

if __name__ == "__main__":
    generate_report()
```

---

### Script 10: Backup Automator

backs up your data and state directories with rotation.

```python
#!/usr/bin/env python3
"""backup_automator.py - backup data and state with rotation"""

import os
import shutil
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")
STATE_DIR = os.getenv("STATE_DIR", "./state")
BACKUP_DIR = os.getenv("BACKUP_DIR", "./backups")
MAX_BACKUPS = int(os.getenv("MAX_BACKUPS", "7"))  # keep last 7

def create_backup():
    """create a timestamped backup of data and state"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{timestamp}")

    os.makedirs(backup_path, exist_ok=True)

    dirs_to_backup = [
        ("data", DATA_DIR),
        ("state", STATE_DIR),
    ]

    total_files = 0
    total_size = 0

    for name, source_dir in dirs_to_backup:
        if not os.path.exists(source_dir):
            continue

        dest = os.path.join(backup_path, name)
        shutil.copytree(source_dir, dest)

        for root, dirs, files in os.walk(dest):
            for f in files:
                total_files += 1
                total_size += os.path.getsize(os.path.join(root, f))

    # write manifest
    manifest = {
        "timestamp": timestamp,
        "created_at": datetime.now().isoformat(),
        "total_files": total_files,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "directories": [d[0] for d in dirs_to_backup if os.path.exists(d[1])]
    }

    with open(os.path.join(backup_path, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    return backup_path, manifest

def rotate_backups():
    """remove old backups, keep only MAX_BACKUPS most recent"""
    if not os.path.exists(BACKUP_DIR):
        return 0

    backups = sorted([
        d for d in os.listdir(BACKUP_DIR)
        if d.startswith("backup_") and os.path.isdir(os.path.join(BACKUP_DIR, d))
    ])

    removed = 0
    while len(backups) > MAX_BACKUPS:
        oldest = backups.pop(0)
        shutil.rmtree(os.path.join(BACKUP_DIR, oldest))
        removed += 1

    return removed

def main():
    print(f"creating backup at {datetime.now().isoformat()}")

    backup_path, manifest = create_backup()
    print(f"  backup created: {backup_path}")
    print(f"  files: {manifest['total_files']}, size: {manifest['total_size_mb']} MB")

    removed = rotate_backups()
    if removed:
        print(f"  rotated: {removed} old backups removed (keeping {MAX_BACKUPS})")

    print("done.")

if __name__ == "__main__":
    main()
```

---

## Part 3: Cron Setup Guide

cron runs your scripts automatically on a schedule. set it once, forget it.

### macOS / Linux

open your crontab:
```bash
crontab -e
```

add entries (one per line):
```bash
# run web scraper every 6 hours
0 */6 * * * cd /path/to/my-automations && /path/to/venv/bin/python3 scripts/web_scraper.py >> logs/scraper.log 2>&1

# run API poller every hour
0 * * * * cd /path/to/my-automations && /path/to/venv/bin/python3 scripts/api_poller.py >> logs/poller.log 2>&1

# run file monitor every 30 minutes
*/30 * * * * cd /path/to/my-automations && /path/to/venv/bin/python3 scripts/file_monitor.py >> logs/monitor.log 2>&1

# generate daily report at 8am
0 8 * * * cd /path/to/my-automations && /path/to/venv/bin/python3 scripts/report_generator.py >> logs/report.log 2>&1

# backup daily at midnight
0 0 * * * cd /path/to/my-automations && /path/to/venv/bin/python3 scripts/backup_automator.py >> logs/backup.log 2>&1

# send alert digest at 9am
0 9 * * * cd /path/to/my-automations && /path/to/venv/bin/python3 scripts/alert_sender.py >> logs/alerts.log 2>&1
```

### cron format cheat sheet

```
* * * * *
| | | | |
| | | | +-- day of week (0-7, 0=Sunday)
| | | +---- month (1-12)
| | +------ day of month (1-31)
| +-------- hour (0-23)
+---------- minute (0-59)
```

common patterns:
- `*/5 * * * *` = every 5 minutes
- `0 * * * *` = every hour
- `0 */6 * * *` = every 6 hours
- `0 8 * * *` = daily at 8am
- `0 8 * * 1-5` = weekdays at 8am
- `0 0 * * 0` = weekly on Sunday at midnight

### Windows (Task Scheduler)

1. open Task Scheduler
2. create Basic Task
3. set trigger (daily, hourly, etc.)
4. action: Start a Program
5. program: `C:\path\to\venv\Scripts\python.exe`
6. arguments: `scripts\web_scraper.py`
7. start in: `C:\path\to\my-automations`

### debugging cron

```bash
# check if cron is running
crontab -l

# check cron logs (macOS)
log show --predicate 'process == "cron"' --last 1h

# test a cron command manually first
cd /path/to/my-automations && /path/to/venv/bin/python3 scripts/web_scraper.py
```

---

## Part 4: Claude Code Overnight Loop

the most powerful automation in this kit. give Claude Code a task list, let it run all night, wake up to completed work.

### the concept

Claude Code can run in a loop: read instructions, execute a task, save results, move to next task. each iteration gets fresh context but reads state from the filesystem. this means it can work for 8+ hours without losing track of what it's done.

### the PROMPT.md file

create a file called `PROMPT.md` in your project root:

```markdown
# overnight task list

## instructions
- read STATE.md to see what's been completed
- pick the NEXT uncompleted task
- complete it fully
- update STATE.md with results
- exit cleanly

## tasks

1. [ ] scrape the top 50 results for "best CRM for startups" and save to data/crm_research.md
2. [ ] write 5 twitter posts about CRM comparisons, save to data/content_queue/
3. [ ] analyze data/raw_leads.csv and create a scoring report
4. [ ] generate email templates for each lead segment
5. [ ] create a competitive analysis of the top 5 CRMs

## rules
- one task per iteration
- save all output to files (filesystem = memory)
- update STATE.md after each task
- if a task fails, note the error in STATE.md and move on
```

### the STATE.md file

```markdown
# overnight loop state

## completed
(none yet)

## current
(none)

## errors
(none)
```

### the loop script

```bash
#!/bin/bash
# overnight_loop.sh - run Claude Code in a loop

PROJECT_DIR="/path/to/my-automations"
MAX_ITERATIONS=20
ITERATION=0

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    echo "--- iteration $ITERATION at $(date) ---"

    # run claude code with the prompt
    cat "$PROJECT_DIR/PROMPT.md" | claude --dangerously-skip-permissions --print \
        --project-dir "$PROJECT_DIR"

    ITERATION=$((ITERATION + 1))

    # check if all tasks are done
    if grep -q "all tasks completed" "$PROJECT_DIR/STATE.md" 2>/dev/null; then
        echo "all tasks completed at iteration $ITERATION"
        break
    fi

    # small pause between iterations
    sleep 5
done

echo "loop finished after $ITERATION iterations"
```

### running it

```bash
chmod +x overnight_loop.sh
# run at night, results in the morning
nohup ./overnight_loop.sh > logs/overnight.log 2>&1 &
```

### key principles

1. **filesystem is memory.** Claude Code doesn't remember between iterations. every piece of state goes in a file. STATE.md, data files, output files. if it's not on disk, it doesn't exist.

2. **one task per iteration.** don't try to do everything at once. each iteration: read state, do one task, write results, exit. the loop handles repetition.

3. **state must be explicit.** STATE.md should tell the next iteration exactly what's done, what's next, and what failed. no ambiguity.

4. **fail forward.** if a task fails, log the error and move to the next one. don't let one failure stop the entire overnight run.

5. **cap iterations.** always set MAX_ITERATIONS. an infinite loop that runs into an error state will burn API credits until you wake up and kill it.

---

## Part 5: Filesystem-as-Memory Pattern

the biggest problem with AI agents: they forget everything between sessions. this pattern solves it using your hard drive.

### the core idea

instead of trying to keep everything in context, write important state to files. next session, read the files. your filesystem becomes the agent's long-term memory.

### memory file types

```
state/
  current_task.md      # what the agent is working on right now
  completed_tasks.md   # what's been done
  decisions.md         # why certain choices were made
  errors.md            # what failed and why
  context.md           # important context that shouldn't be lost
  preferences.md       # user preferences and configurations
```

### the pattern in code

```python
import os
import json
from datetime import datetime

STATE_DIR = "./state"

def read_memory(key):
    """read a memory file"""
    filepath = os.path.join(STATE_DIR, f"{key}.md")
    if os.path.exists(filepath):
        with open(filepath) as f:
            return f.read()
    return ""

def write_memory(key, content, append=False):
    """write or append to a memory file"""
    filepath = os.path.join(STATE_DIR, f"{key}.md")
    os.makedirs(STATE_DIR, exist_ok=True)

    mode = "a" if append else "w"
    timestamp = datetime.now().isoformat()

    with open(filepath, mode) as f:
        if append:
            f.write(f"\n---\n[{timestamp}]\n{content}\n")
        else:
            f.write(f"# {key}\n_updated: {timestamp}_\n\n{content}\n")

def log_decision(decision, reasoning):
    """log a decision with reasoning for future reference"""
    entry = f"**Decision:** {decision}\n**Reasoning:** {reasoning}"
    write_memory("decisions", entry, append=True)

def log_error(task, error):
    """log an error for debugging"""
    entry = f"**Task:** {task}\n**Error:** {error}"
    write_memory("errors", entry, append=True)

# usage:
# write_memory("current_task", "processing lead batch 3 of 7")
# write_memory("completed_tasks", "- batch 1: 50 leads\n- batch 2: 47 leads", append=True)
# log_decision("skipped API endpoint X", "rate limit hit, will retry tomorrow")
```

### why this works

- **survives crashes.** filesystem doesn't lose data when your script crashes.
- **survives context resets.** new Claude Code session? read the files, pick up where you left off.
- **auditable.** you can read the files yourself and see exactly what happened.
- **no database needed.** markdown files on disk. simple. works everywhere.
- **version controlled.** commit state files to git and you have full history.

---

## Part 6: 5 Automation Recipes

### Recipe 1: Lead Generation Pipeline

scripts used: web_scraper + lead_processor + csv_aggregator + alert_sender

```
cron (every 6 hours)
  -> web_scraper.py scrapes job boards, directories
  -> saves raw data to data/raw_leads.csv
  -> lead_processor.py cleans and scores
  -> csv_aggregator.py merges into master
  -> alert_sender.py notifies if high-score leads found
```

### Recipe 2: Content Farm

scripts used: content_scheduler + file_monitor + report_generator

```
you write posts -> drop .txt files in data/content_queue/
  -> file_monitor.py detects new files
  -> content_scheduler.py assigns posting times
  -> (connect to Buffer/Typefully API to auto-post)
  -> report_generator.py tracks queue depth
```

### Recipe 3: Competitor Monitor

scripts used: web_scraper + file_monitor + alert_sender

```
cron (every 2 hours)
  -> web_scraper.py checks competitor pages
  -> file_monitor.py detects changes in scraped data
  -> alert_sender.py sends "competitor changed pricing" alert
  -> you react before they get ahead
```

### Recipe 4: Research Aggregator

scripts used: api_poller + data_cleaner + csv_aggregator + report_generator

```
cron (daily)
  -> api_poller.py collects data from multiple sources
  -> data_cleaner.py normalizes formats
  -> csv_aggregator.py combines into research database
  -> report_generator.py creates daily research brief
```

### Recipe 5: Financial Tracker

scripts used: api_poller + report_generator + alert_sender + backup_automator

```
cron (daily at market close)
  -> api_poller.py grabs prices/balances
  -> report_generator.py creates P&L summary
  -> alert_sender.py sends if thresholds crossed
  -> backup_automator.py saves everything
```

---

## what to do now

1. set up your environment (Part 1). 10 minutes.
2. pick ONE script. run it manually. make sure it works.
3. set up a cron job for that script.
4. add a second script. chain them into a recipe.
5. set up the overnight loop when you're comfortable with the basics.

the goal is not to run all 10 scripts on day one. the goal is to have one automation running by tonight. then build from there.

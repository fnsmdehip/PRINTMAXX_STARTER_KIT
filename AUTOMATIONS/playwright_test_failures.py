#!/usr/bin/env python3
import subprocess
from pathlib import Path

REPORTS_DIR = Path("/Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/AUTOMATIONS/agent/swarm/reports")

# Sites that returned 000 or 404
FAILURES = [
    "couples-streak.surge.sh",
    "handyman-pensacola-fl-ace-handyman-services-pensacola-pensacola-fl.surge.sh",
    "lemlist-vs-instantly.surge.sh",
    "klaviyo-alternative.surge.sh",
    "pocket-alexandria.surge.sh",
]

def detailed_test(url):
    """More detailed diagnostic"""
    # Try with longer timeout and verbose output
    cmd = f"curl -v 'https://{url}' -m 10 2>&1 | head -30"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

print("[FAILURE DIAGNOSTICS]\n")

for url in FAILURES:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    # Try DNS resolution
    dns_cmd = f"nslookup {url.split('.')[0]}.surge.sh 8.8.8.8"
    dns_result = subprocess.run(dns_cmd, shell=True, capture_output=True, text=True)
    
    # Try curl with diagnostic
    curl_cmd = f"curl -I 'https://{url}' -m 3 2>&1"
    curl_result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True)
    
    print(f"\nDNS Lookup:")
    print(dns_result.stdout[:200] if dns_result.stdout else dns_result.stderr[:200])
    
    print(f"\nHTTP HEAD:")
    print(curl_result.stdout + curl_result.stderr)

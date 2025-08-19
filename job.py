import requests
import os
import difflib
from datetime import datetime

# Step 1: Fetch HTML
url = "https://www.taylorswift.com"
try:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    html_content = response.text
except requests.RequestException as e:
    print(f"[{datetime.utcnow()}] Error fetching {url}: {e}")
    exit(1)

# Step 2: Compare with stored HTML
html_file = "site.html"

if not os.path.exists(html_file):
    # If file doesn't exist, create it
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[{datetime.utcnow()}] HTML file created.")
else:
    # If file exists, compare old and new
    with open(html_file, "r", encoding="utf-8") as f:
        old_html = f.readlines()
    
    new_html = html_content.splitlines(keepends=True)

    if old_html == new_html:
        print(f"[{datetime.utcnow()}] HTML is the same. No changes detected.")
    else:
        print(f"[{datetime.utcnow()}] HTML changed! Here's the diff:")
        diff = difflib.unified_diff(
            old_html,
            new_html,
            fromfile='old_site.html',
            tofile='new_site.html',
            lineterm=''
        )
        for line in diff:
            print(line)

        # Save the new HTML
        with open(html_file, "w", encoding="utf-8") as f:
            f.writelines(new_html)

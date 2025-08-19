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
        old_html = f.read()

    # Calculate similarity
    similarity = difflib.SequenceMatcher(None, old_html, html_content).ratio()
    percent_diff = (1 - similarity) * 100

    print(f"[{datetime.utcnow()}] HTML percent difference: {percent_diff:.2f}%")

    # Save the new HTML
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

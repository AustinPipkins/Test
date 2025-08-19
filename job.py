import requests
import os
import difflib
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Email config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
SEND_TO_EMAIL = os.environ["SEND_TO_EMAIL"]
EMAIL_SUBJECT = "Taylor Swift site changed!"

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
commit_threshold = 1.0  # percent
email_threshold = 0.0  # percent

commit_needed = False
send_email = False

if not os.path.exists(html_file):
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[{datetime.utcnow()}] HTML file created. Will commit and potentially email.")
    commit_needed = True
else:
    with open(html_file, "r", encoding="utf-8") as f:
        old_html = f.read()

    similarity = difflib.SequenceMatcher(None, old_html, html_content).ratio()
    percent_diff = (1 - similarity) * 100
    print(f"[{datetime.utcnow()}] HTML percent difference: {percent_diff:.2f}%")

    if percent_diff >= commit_threshold:
        commit_needed = True
        print(f"[{datetime.utcnow()}] Change exceeds commit threshold. Will commit.")
    if percent_diff >= email_threshold:
        send_email = True
        print(f"[{datetime.utcnow()}] Change exceeds email threshold. Will send email.")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

# Step 3: Send email if needed
if send_email:
    msg_body = f"Taylor Swift site changed!\nPercent difference: {percent_diff:.2f}%\nChecked at {datetime.utcnow()}"
    msg = MIMEText(msg_body)
    msg["From"] = EMAIL_USER
    msg["To"] = SEND_TO_EMAIL
    msg["Subject"] = EMAIL_SUBJECT

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, SEND_TO_EMAIL, msg.as_string())
        server.quit()
        print(f"[{datetime.utcnow()}] Email sent to {SEND_TO_EMAIL}")
    except Exception as e:
        print(f"[{datetime.utcnow()}] Failed to send email: {e}")

# Step 4: Exit code for workflow
if commit_needed:
    exit(0)
else:
    exit(1)

import requests
import hashlib
import os

# Step 1: Fetch HTML
url = "https://www.taylorswift.com"
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise error if request failed
    html_content = response.text
except requests.RequestException as e:
    print(f"Error fetching {url}: {e}")
    exit(1)

# Step 2: Hash the HTML
current_hash = hashlib.sha256(html_content.encode("utf-8")).hexdigest()

# Step 3: Compare with stored hash
hash_file = "hash.txt"

if not os.path.exists(hash_file):
    # If file doesn't exist, create and store hash
    with open(hash_file, "w") as f:
        f.write(current_hash)
    print("Hash file created.")
else:
    # If file exists, read old hash and compare
    with open(hash_file, "r") as f:
        old_hash = f.read().strip()

    if current_hash == old_hash:
        print("Hashes are the same. No changes detected.")
    else:
        print("Hashes are different! Updating hash file.")
        with open(hash_file, "w") as f:
            f.write(current_hash)

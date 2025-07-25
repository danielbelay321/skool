import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get token from environment variable
auth_token = os.getenv("AUTH_TOKEN")

if not auth_token:
    raise ValueError("No AUTH_TOKEN found in environment variables. Please set it in your .env file.")

# Setup
options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # adjust path as needed
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Navigate and authenticate
driver.get("https://www.skool.com/coder")
driver.add_cookie({
    "name": "auth_token",
    "value": auth_token,
    "domain": "www.skool.com",
    "path": "/"
})

driver.get("https://www.skool.com/coder")
time.sleep(5)

# Extract __NEXT_DATA__ JSON
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

next_data_script = soup.find("script", {"id": "__NEXT_DATA__"})
if not next_data_script:
    print("❌ Couldn't find __NEXT_DATA__ script tag.")
    exit()

next_data = json.loads(next_data_script.string)

# Navigate to posts
try:
    post_trees = next_data["props"]["pageProps"]["postTrees"]
    print(f"✅ Found {len(post_trees)} posts")

    for post_tree in post_trees:
        post = post_tree.get("post", {})
        title = post.get("name")
        content = post.get("metadata", {}).get("content", "")[:100]  # truncate for display
        post_id = post.get("id")
        post_url = f"https://www.skool.com/coder/{post_id}"
        print(f"\n📝 {title}\n🔗 {post_url}\n📄 {content}\n")

except KeyError as e:
    print(f"❌ JSON structure unexpected. Missing key: {e}")

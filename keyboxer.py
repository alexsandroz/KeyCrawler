import os

import requests
from dotenv import load_dotenv
from lxml import etree

from check import keybox_check
from helpers import CACHE_FILE, SAVE_DIR, hash_xml_file

session = requests.Session()

# Load environment variables from .env file
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set in the .env file")

# Search query
SEARCH_QUERY = "<AndroidAttestation>+-repo:pperez39/google-keys"
SEARCH_URL = f"https://api.github.com/search/code?q={SEARCH_QUERY}"

# Headers for the API request
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

cached_urls = set(open(CACHE_FILE, "r").readlines())


class RateLimitError(Exception):
    def __init__(self, message, resume_epoch):
        from datetime import timezone

        super().__init__(message)
        self.resume_epoch = resume_epoch

    def get_sleep_time(self):
        from datetime import datetime, timezone

        tz = timezone.utc
        return abs(datetime.fromtimestamp(self.resume_epoch, tz=tz) - datetime.now(tz=tz)).total_seconds()


# Function to fetch and print search results
def fetch_and_process_results(page: int) -> bool:
    params = {"per_page": 100, "page": page}
    response = session.get(SEARCH_URL, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Failed to retrieve search results: {response.status_code}")
        # print(f"url: {search_url}, presponse headers: {response.headers}")
        print(f"response: {response.text}")
        if response.headers.get("X-RateLimit-Reset") and response.status_code == 403:
            reset_time = response.headers["X-RateLimit-Reset"]
            raise RateLimitError("Rate limit exceeded. Please try again later.", resume_epoch=int(reset_time))
        else:
            raise RuntimeError()

    search_results = response.json()
    if "items" in search_results:
        for item in search_results["items"]:
            file_name = item["name"]
            # Process only XML files
            if file_name.lower().endswith(".xml"):
                raw_url: str = (
                    item["html_url"].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                )
                # check if the file exists in cache
                if raw_url + "\n" in cached_urls:
                    continue
                else:
                    cached_urls.add(raw_url + "\n")
                # Fetch the file content
                file_content = fetch_file_content(raw_url)
                # Parse the XML
                try:
                    file_name = hash_xml_file(file_content)
                except etree.XMLSyntaxError:
                    continue
                file_name_save = SAVE_DIR / file_name
                if not file_name_save.exists() and file_content and keybox_check(file_content):
                    print(f"{raw_url} is new")
                    with open(file_name_save, "wb") as f:
                        f.write(file_content)
    return len(search_results["items"]) > 0  # Return True if there could be more results


# Function to fetch file content
def fetch_file_content(url: str) -> bytes:
    response = session.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise RuntimeError(f"Failed to download {url}")


# Fetch all pages
page = 1
has_more_results = True
while has_more_results:
    try:
        has_more_results = fetch_and_process_results(page)
        page += 1
    except RateLimitError as e:
        print(f"Rate limit exceeded. Retrying after {e.get_sleep_time()}...")
        import time

        time.sleep(e.get_sleep_time())
        print("Retrying...")
    except RuntimeError as e:
        print("Error during fetching results, saving cache and checking files")
        break


# update cache
open(CACHE_FILE, "w").writelines(cached_urls)

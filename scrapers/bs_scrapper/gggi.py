import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging

# Optional: Fake User Agent
try:
    from fake_useragent import UserAgent
except ImportError:
    UserAgent = None  # Handle fallback if module is missing

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Open keywords for GGGI
open_keywords = [
    "call for project concept notes",
    "submit via email"
]

# Get user-agent string
def get_user_agent():
    if UserAgent:
        try:
            ua = UserAgent()
            return ua.random
        except Exception as e:
            logger.warning("Failed to fetch user-agent from UserAgent. Using fallback.")
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36"

# Check if grant is open
def is_grant_open(text):
    text = text.lower()

    # Keyword check
    has_open_keyword = any(keyword in text for keyword in open_keywords)
    if not has_open_keyword:
        return False

    # Date sanity check (avoid outdated posts)
    date_match = re.search(r'(\d{1,2} \w+ \d{4})', text)
    if date_match:
        try:
            found_date = datetime.strptime(date_match.group(1), "%d %B %Y")
            if found_date < datetime.utcnow():
                return False  # Outdated
        except ValueError:
            pass  # Parsing failed; ignore

    return True

# Main scraping function
def scrape_gggi(url="https://gggi.org/tag/grants/"):
    headers = {'User-Agent': get_user_agent()}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        text = BeautifulSoup(res.text, 'html.parser').get_text()
        status = 'open' if is_grant_open(text) else 'closed'
        return {'url': url, 'status': status}
    except Exception as e:
        return {'url': url, 'status': 'error', 'error': str(e)}

# # Example usage
# if __name__ == "__main__":
#     result = scrape_gggi()
#     print(result)

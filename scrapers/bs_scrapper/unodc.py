import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging

# Try optional fake user-agent for realism
try:
    from fake_useragent import UserAgent
except ImportError:
    UserAgent = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom open keywords specific to UNODC
open_keywords = [
    "applications are open",
    "apply now",
    "now open",
    "submission deadline"
]

# Function to get a random user agent
def get_user_agent():
    if UserAgent:
        try:
            ua = UserAgent()
            return ua.random
        except Exception as e:
            logger.warning("Failed to use fake_useragent. Using fallback. Error: %s", e)
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36"

# Function to determine if a grant is open
def is_grant_open(text):
    text = text.lower()
    
    # Keyword-based filter
    has_open_keyword = any(keyword in text for keyword in open_keywords)
    if not has_open_keyword:
        return False

    # Date validation to avoid stale posts
    date_match = re.search(r'(\d{1,2} \w+ \d{4})', text)
    if date_match:
        try:
            found_date = datetime.strptime(date_match.group(1), "%d %B %Y")
            if found_date < datetime.utcnow():
                return False  # Date is in the past
        except ValueError:
            pass  # Invalid date format

    return True

# Scraping function for UNODC
def scrape_unodc(url="https://www.unodc.org/unodc/en/human-trafficking-fund/unvtf-funding.html"):
    headers = {'User-Agent': get_user_agent()}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        text = BeautifulSoup(res.text, 'html.parser').get_text()
        status = 'open' if is_grant_open(text) else 'closed'
        return {'url': url, 'status': status}
    except Exception as e:
        return {'url': url, 'status': 'error', 'error': str(e)}

# Example usage
# if __name__ == "__main__":
#     result = scrape_unodc()
#     print(result)

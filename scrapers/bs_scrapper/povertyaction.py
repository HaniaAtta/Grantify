import logging
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Keywords specific to Poverty Action grants
open_keywords = [
    "call for proposals",
    "applications are open",
    "request for applications"
]

# Function to generate a user-agent string
def get_user_agent():
    try:
        ua = UserAgent()
        return ua.random
    except Exception as e:
        logger.warning("Failed to get UserAgent: %s", e)
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36"

# Function to determine if a grant is open
def is_grant_open(text):
    text = text.lower()
    has_open_keyword = any(keyword in text for keyword in open_keywords)
    if not has_open_keyword:
        return False

    # Optional: date check to avoid stale announcements
    date_match = re.search(r'(\d{1,2} \w+ \d{4})', text)
    if date_match:
        try:
            found_date = datetime.strptime(date_match.group(1), "%d %B %Y")
            if found_date < datetime.utcnow():
                return False
        except ValueError:
            pass

    return True

# Main scraping function
def scrape_poverty_action(url="https://poverty-action.org/open-funding-opportunities"):
    headers = {'User-Agent': get_user_agent()}
    try:
        res = requests.get(url, headers=headers, timeout=20)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text()
        status = 'open' if is_grant_open(text) else 'closed'
        return {'url': url, 'status': status}
    except Exception as e:
        logger.error("Error occurred while scraping Poverty Action: %s", e)
        return {'url': url, 'status': 'error', 'error': str(e)}

# Entry point
# if __name__ == "__main__":
#     result = scrape_poverty_action()
#     print(result)

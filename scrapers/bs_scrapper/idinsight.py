import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging

# Optional fake user-agent
try:
    from fake_useragent import UserAgent
except ImportError:
    UserAgent = None  # Fallback if not installed

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom open keywords for IDinsight
open_keywords = [
    "call for proposals",
    "request for proposals",
    "applications are open",
    "apply now",
    "deadline to apply"
]

# Function to generate a user agent
def get_user_agent():
    if UserAgent:
        try:
            ua = UserAgent()
            return ua.random
        except Exception as e:
            logger.warning("Using fallback User-Agent due to error: %s", e)
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36"

# Function to check if grant is open
def is_grant_open(text):
    text = text.lower()
    
    has_open_keyword = any(keyword in text for keyword in open_keywords)
    if not has_open_keyword:
        return False

    # Optional: Check for past dates
    date_match = re.search(r'(\d{1,2} \w+ \d{4})', text)
    if date_match:
        try:
            found_date = datetime.strptime(date_match.group(1), "%d %B %Y")
            if found_date < datetime.utcnow():
                return False  # Old date
        except ValueError:
            pass  # Ignore parsing errors

    return True

# Main scraping function for IDinsight
def scrape_idinsight(url="https://www.idinsight.org/article/call-for-proposals-advancing-evidence-on-digital-platform-work-in-lmics/"):
    headers = {'User-Agent': get_user_agent()}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        text = BeautifulSoup(res.text, 'html.parser').get_text()
        status = 'open' if is_grant_open(text) else 'closed'
        return {'url': url, 'status': status}
    except Exception as e:
        return {'url': url, 'status': 'error', 'error': str(e)}


import logging
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session = requests.Session()

open_keywords = [
   'submit a grant', 'accepting proposals', 'open', 'now open', 'currently open',
   'applications open', 'accepting applications', 'application window open',
   'available', 'apply now', 'submissions open', 'call for proposals',
   'funding available', 'enrollment open', 'opportunity open',
   'accepting submissions', 'now accepting applications', 'call open',
   'rfa open', 'cfp open', 'solicitation open', 'registration open',
   'live', 'active', 'ongoing', 'deadline', 'closing date', 'forthcoming',
   'open for submission', 'now accepting applications', 'open call',
   
]

def get_user_agent():
    try:
        ua = UserAgent()
        return ua.random
    except:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36"

def is_grant_open(text):
    text = text.lower()

    # Check if text contains a keyword suggesting it's open
    has_open_keyword = any(keyword in text for keyword in open_keywords)

    if not has_open_keyword:
        return False

    # Try to catch a date like "20 June 2021"
    date_match = re.search(r'(\d{1,2} \w+ \d{4})', text)
    if date_match:
        try:
            found_date = datetime.strptime(date_match.group(1), "%d %B %Y")
            if found_date < datetime.utcnow():
                # The keyword might be stale — old date!
                return False
        except ValueError:
            pass  # In case parsing fails

    return True

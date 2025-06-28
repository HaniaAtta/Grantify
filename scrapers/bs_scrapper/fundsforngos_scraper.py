import requests
from bs4 import BeautifulSoup
from scrapers.utils import get_user_agent, is_grant_open 

def scrape_fundsforngos(url="https://www.fundsforngos.org/"):
    headers = {'User-Agent': get_user_agent()}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        text = BeautifulSoup(res.text, 'html.parser').get_text()
        return {'url': url, 'status': 'open' if is_grant_open(text) else 'closed'}
    except Exception as e:
        return {'url': url, 'status': 'error', 'error': str(e)}

# import requests
# from bs4 import BeautifulSoup
# import random

# # Example User-Agent list for get_user_agent
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
#     " Chrome/58.0.3029.110 Safari/537.3",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)"
#     " Version/14.0 Safari/605.1.15",
#     # Add more user agents as needed
# ]

# def get_user_agent():
#     """Return a random user-agent string."""
#     return random.choice(USER_AGENTS)

# def is_grant_open(text):
#     """
#     Dummy implementation:
#     Check if grant is open by searching keywords in page text.
#     Replace with your actual logic.
#     """
#     keywords_open = ["apply now", "open for applications", "deadline", "submit a grant"]
#     text_lower = text.lower()
#     return any(keyword in text_lower for keyword in keywords_open)

# def scrape_fundsforngos():
#     url = "https://www.fundsforngos.org/"
#     headers = {'User-Agent': get_user_agent()}
#     try:
#         res = requests.get(url, headers=headers, timeout=10)
#         res.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
#         text = BeautifulSoup(res.text, 'html.parser').get_text(separator=' ')
#         status = 'open' if is_grant_open(text) else 'closed'
#         return {'url': url, 'status': status}
#     except Exception as e:
#         return {'url': url, 'status': 'error', 'error': str(e)}

# if __name__ == "__main__":
#     result = scrape_fundsforngos()
#     print(result)

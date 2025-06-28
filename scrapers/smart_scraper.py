import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapers.utils import is_grant_open, get_user_agent

def smart_scrape(url):
    headers = {'User-Agent': get_user_agent()}
    
    # Try BeautifulSoup
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        status = 'open' if is_grant_open(text) else 'closed'
        return {'url': url, 'status': status}
    except Exception as bs_err:
        pass  # fallback to Selenium

    # Fallback: Selenium
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        text = driver.page_source
        driver.quit()
        status = 'open' if is_grant_open(text) else 'closed'
        return {'url': url, 'status': status}
    except Exception as sel_err:
        try:
            driver.quit()
        except:
            pass
        return {'url': url, 'status': 'error', 'error': str(sel_err)}

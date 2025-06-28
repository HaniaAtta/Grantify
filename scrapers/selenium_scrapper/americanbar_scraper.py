# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from scrapers.utils import get_user_agent, is_grant_open


# def scrape_americanbar():
#     url = "https://www.americanbar.org/membership/"
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")

#     try:
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=options)
#         driver.get(url)
#         text = driver.page_source
#         driver.quit()
#         status = 'open' if is_grant_open(text) else 'closed'
#         return {'url': url, 'status': status}
#     except Exception as e:
#         try: driver.quit()
#         except: pass
#         return {'url': url, 'status': 'error', 'error': str(e)}

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapers.utils import get_user_agent, is_grant_open

def scrape_americanbar(url="https://www.americanbar.org/membership/"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        text = driver.page_source
        status = 'open' if is_grant_open(text) else 'closed'
        return {'url': url, 'status': status}
    except Exception as e:
        return {'url': url, 'status': 'error', 'error': str(e)}
    finally:
        if driver:
            driver.quit()

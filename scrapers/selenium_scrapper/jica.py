from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapers.utils import is_grant_open

def scrape_jica(url = "https://www.jica.go.jp/english/"):
    
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        text = driver.page_source

        driver.quit()

        status = 'open' if is_grant_open(text) else 'closed'
        return {'url': url, 'status': status}

    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        return {'url': url, 'status': 'error', 'error': str(e)}

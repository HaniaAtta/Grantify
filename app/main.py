from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from urllib.parse import urlparse
from app.database import create_database, add_grant, get_grants, url_exists
from app.utils.email_sender import send_email
from fastapi.staticfiles import StaticFiles
from scrapers.smart_scraper import smart_scrape
import redis
import traceback

# Init app
app = FastAPI()

templates = Jinja2Templates(directory="app/templates")
app.mount("/image", StaticFiles(directory="app/image"), name="image")

create_database()
print("[INIT] Database created or already exists.")

# Pydantic model
class URLRequest(BaseModel):
    url: str

# Connect to Redis
# Connect to Redis
try:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)  # 👈 This is the line
    redis_client.ping()
    print("[INFO] Redis connected successfully.")
except redis.ConnectionError as e:
    print("[ERROR] Redis connection error:", e)
    redis_client = None


@app.post("/api/check_url")
async def check_url(data: URLRequest):
    url = data.url
    domain = urlparse(url).netloc.replace("www.", "")

    print(f"[DEBUG] Received URL to check: {url}")
    print(f"[DEBUG] Extracted domain: {domain}")

    from scrapers.router import SCRAPER_ROUTER
    scraper_func = SCRAPER_ROUTER.get(domain)
    
    if not scraper_func:
        print(f"[WARNING] No scraper function found for domain: {domain}")
        return JSONResponse(
            content={"url": url, "status": "error", "reason": "No scraper found for this domain"},
            status_code=400
        )

    try:
        print(f"[INFO] Running scraper for domain: {domain}")
        result = scraper_func()
        print(f"[DEBUG] Scraper result for {url}: {result}")
    except Exception as e:
        print(f"[ERROR] Exception while scraping {url}:\n{traceback.format_exc()}")
        return JSONResponse(
            content={"url": url, "status": "error", "reason": f"Scraping error: {str(e)}"},
            status_code=500
        )

    if result["status"] == "open":
        print(f"[INFO] Grant is open for {url}. Sending email and saving to DB.")
        send_email(
            subject="Grant Open Notification",
            body=f"Grant is open at: {url}",
            to_email="attahania193@gmail.com"
        )
        add_grant(url, result["status"])
    else:
        print(f"[INFO] Grant status is not open for {url}: {result['status']}")

    return JSONResponse(content=result)

@app.post("/api/scrape_all")
async def scrape_all():
    print("[INFO] /api/scrape_all triggered. Importing and calling Celery task...")
    try:
        from tasks.run_scrapers import run_all_scrapers
        print("[DEBUG] Calling run_all_scrapers.delay()...")
        run_all_scrapers.delay()
        print("[INFO] Celery task run_all_scrapers triggered successfully.")
        return {"message": "Scraping started in background"}
    except Exception as e:
        print(f"[ERROR] Failed to trigger Celery task:\n{traceback.format_exc()}")
        return JSONResponse(
            content={"status": "error", "message": "Failed to start scraping task"},
            status_code=500
        )

@app.post("/api/submit-url")
async def submit_url(data: URLRequest):
    url = data.url.strip()
    print(f"[DEBUG] /api/submit-url received: {url}")

    if url_exists(url):
        print(f"[INFO] URL already exists in database: {url}")
        return JSONResponse({"status": "exists", "message": "URL already exists in the database."})

    try:
        print(f"[INFO] Running smart_scrape for: {url}")
        result = smart_scrape(url)
        print(f"[DEBUG] smart_scrape result: {result}")
    except Exception as e:
        print(f"[ERROR] smart_scrape failed:\n{traceback.format_exc()}")
        return JSONResponse({"status": "error", "message": "Scraping failed with exception."})

    if result["status"] == "error":
        return JSONResponse({"status": "error", "message": result.get("error", "Scraping failed")})

    add_grant(url, result["status"])
    print(f"[INFO] Grant added to database: {url} -> {result['status']}")

    return JSONResponse({
        "status": "success",
        "message": f"URL scraped and added with status: {result['status']}",
        "url": url,
        "scrape_status": result["status"]
    })
@app.delete("/api/remove-url/{grant_id}")
async def remove_url(grant_id: int):
    from app.database import remove_grant_by_id

    try:
        print(f"[INFO] Deleting grant with ID: {grant_id}")
        remove_grant_by_id(grant_id)
        return JSONResponse(content={"status": "success", "message": "Grant removed successfully."})
    except Exception as e:
        print(f"[ERROR] Failed to delete grant ID {grant_id}: {e}")
        return JSONResponse(
            content={"status": "error", "message": "Failed to remove grant."},
            status_code=500
        )

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    print("[INFO] Root route accessed, fetching grants from database.")
    grants = get_grants()
    total_grants = len(grants)
    open_count = sum(1 for g in grants if g[2] == "open")
    closed_count = sum(1 for g in grants if g[2] == "closed")

    print(f"[DEBUG] Total: {total_grants}, Open: {open_count}, Closed: {closed_count}")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "grants": grants,
        "total_grants": total_grants,
        "open_count": open_count,
        "closed_count": closed_count,
        "current_year": 2025
    })

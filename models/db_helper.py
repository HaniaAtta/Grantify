# models/db_helper.py

from config import SessionLocal
from models.website import Website
from datetime import datetime

def get_all_websites():
    db = SessionLocal()
    websites = db.query(Website).all()
    db.close()
    return websites

def add_website(url: str):
    db = SessionLocal()
    existing = db.query(Website).filter(Website.url == url).first()
    if existing:
        db.close()
        return "Already exists"
    
    new_site = Website(url=url)
    db.add(new_site)
    db.commit()
    db.close()
    return "Added"

def update_status(url: str, status: str):
    db = SessionLocal()
    website = db.query(Website).filter(Website.url == url).first()
    if website:
        website.last_status = status
        website.last_checked = datetime.utcnow()
        db.commit()
    db.close()

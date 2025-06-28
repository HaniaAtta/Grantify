# models/init_db.py

from config import engine, Base
from models.website import Website

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully.")

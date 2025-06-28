import os
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

#db config
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./grants.db")  # Default fallback to SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# celery config
BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("grantly", broker=BROKER_URL, backend=RESULT_BACKEND)
# Add this line here:
celery_app.autodiscover_tasks(['tasks'])

# Main Celery Config
celery_app.conf.update(
    timezone='UTC',
    enable_utc=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

# celery beat
celery_app.conf.beat_schedule = {
    'scrape-every-6-hours': {
        'task': 'tasks.run_scrapers.run_all_scrapers',
        'schedule': crontab(hour='*/6'),
    },
}


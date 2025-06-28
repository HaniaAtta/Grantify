# from tasks.run_scrapers import celery
# from config import celery_app


# if __name__ == '__main__':
#     celery.start()
# from config imput celery_app

# if __name__ == '__main__':
#     pass

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config import celery_app

celery = celery_app

# Optionally, if you want to manually import tasks (instead of autodiscover)
# import tasks.run_scrapers

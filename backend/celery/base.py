import os

from celery import Celery
from dotenv import load_dotenv

CELERY_USER = os.getenv("CELERY_USER")
CELERY_HOST = os.getenv("CELERY_HOST")

load_dotenv(".env")
app = Celery('notify app', broker=f'pyamqp://{CELERY_USER}@{CELERY_HOST}//')

import os
from celery import Celery
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_crawler.settings')

app = Celery('MarketInsight')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Log the broker and backend being used
broker = app.conf.broker_url
backend = app.conf.result_backend
logging.basicConfig(level=logging.INFO)

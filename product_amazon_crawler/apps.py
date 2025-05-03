from django.apps import AppConfig
import threading
from .tasks import check_pool_and_run

class ProductAmazonCrawlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product_amazon_crawler'

    def ready(self):
        threading.Thread(target=check_pool_and_run, daemon=True).start()
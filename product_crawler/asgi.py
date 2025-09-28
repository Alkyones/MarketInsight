import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import product_amazon_crawler.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_crawler.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            product_amazon_crawler.routing.websocket_urlpatterns
        )
    ),
})
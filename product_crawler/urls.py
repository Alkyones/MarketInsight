from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('amazon/', include('product_amazon_crawler.urls'))
]

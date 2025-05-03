from django.contrib import admin
from .models import AmazonDataScrapCollection, ScrapRequest

# Register your models here.

admin.site.register(AmazonDataScrapCollection)
admin.site.register(ScrapRequest)
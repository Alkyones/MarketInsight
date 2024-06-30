from django.urls import path
from . import views

urlpatterns = [
    path('', views.scrapIndex, name='amazon'),
    path('list/', views.scrapedDataList, name='list'),
    path('detail/<str:_id>/', views.scrapedDataDetail, name='detail')
]
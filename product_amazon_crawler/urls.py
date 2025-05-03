from django.urls import path
from . import views

app_name = 'amazon'

urlpatterns = [
    path('', views.scrap_index, name='amazon'),
    path('list/', views.scraped_data_list, name='list'),
    path('request-list/', views.scrap_requests_list, name='request-list'),
    path('scrap-requests/<pk>/status/', views.get_scrap_request_status, name='get_scrap_request_status'),
    path('detail/<str:_id>/', views.scraped_data_detail, name='detail'),
    path('detail/<str:_id>/json', views.scraped_data_detail_json, name='detailJson')
]
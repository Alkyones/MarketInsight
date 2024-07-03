from django.urls import path
from . import views

app_name = 'mainPage'

urlpatterns = [
    path('', views.index, name='index')
]
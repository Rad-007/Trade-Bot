from django.urls import path
from . import views

app_name = 'trading'

urlpatterns = [
    path('', views.index, name='index'),
]

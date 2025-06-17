from django.urls import path
from . import views

app_name = "app_restaurants"

urlpatterns = [
    path('', views.home, name='home'),
    path('api_get_restaurants/', views.api_get_restaurants,name='api_get_restaurants'),
    path('api/cuisine-stats/', views.api_get_cuisine_stats, name='api_get_cuisine_stats'),
]

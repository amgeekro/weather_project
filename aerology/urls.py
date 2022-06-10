from django.urls import path

from .views import weather_views, WeatherAPIViews

urlpatterns = [
    path('', weather_views, name="weather"),
    path('weather-status/', WeatherAPIViews.as_view(), name="weather_api_view"),
]
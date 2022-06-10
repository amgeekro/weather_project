import requests
from django.shortcuts import render
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Weather
from .serializer import WeatherSerializer


def weather_views(request):
    return render(request, 'weather.html')


class WeatherAPIViews(APIView):
    def post(self, request, format=None):
        city = request.data['city']
        if city.isdigit():
            city_code = city
            print("here")
            if cache.get(city_code):
                weather_object = cache.get(city_code)
                print("hit the cache")
            else:
                try:
                    weather_object = Weather.objects.get(city_code=city_code)
                    cache.set(city_code, weather_object)
                except Weather.DoesNotExist:
                    url = f"https://api.openweathermap.org/data/2.5/weather?id={city_code}&appid=df809c6114e74a91627d6ccd77e39d2d"
                    response = requests.get(url)
                    print(response.text)
                    r = response.json()
                    city_code = r["id"]
                    city_name = r["name"]
                    country = r['sys']['country']
                    weather_main = r['weather'][0]['main']
                    weather_desscription = r['weather'][0]['description']
                    temperature = r["main"]['temp']
                    pressure = r["main"]['pressure']
                    humidity = r['main']['humidity']
                    weather_object = Weather.objects.create(city_code=city_code, city_name=city_name, country=country,
                                            weather_main=weather_main, weather_desscription=weather_desscription,
                                            temperature=temperature, pressure=pressure, humidity=humidity)
                    cache.set(city_code, weather_object)

        else:
            city_name = city
            if cache.get(city_name):
                weather_object = cache.get(city_name)
                print("hit the cache")
            else:
                try:
                    weather_object = Weather.objects.get(city_name=city_name)
                    cache.set(city_name, weather_object)
                except Weather.DoesNotExist:
                    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=df809c6114e74a91627d6ccd77e39d2d"
                    response = requests.get(url)
                    print(response.text)
                    r = response.json()
                    city_code = r["id"]
                    city_name = r["name"].lower()
                    country = r['sys']['country']
                    weather_main = r['weather'][0]['main']
                    weather_desscription = r['weather'][0]['description']
                    temperature = r["main"]['temp']
                    pressure = r["main"]['pressure']
                    humidity = r['main']['humidity']
                    weather_object = Weather.objects.create(city_code=city_code, city_name=city_name, country=country,
                                            weather_main=weather_main, weather_desscription=weather_desscription,
                                            temperature=temperature, pressure=pressure, humidity=humidity)
                    cache.set(city_name, weather_object)
    
        serializer = WeatherSerializer(weather_object)
        return Response(serializer.data)




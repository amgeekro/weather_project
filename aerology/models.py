from pyexpat import model
from django.db import models


class Weather(models.Model):
    city_code = models.CharField(max_length=10)
    city_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    weather_main = models.CharField(max_length=50)
    weather_desscription = models.CharField(max_length=50)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    pressure = models.IntegerField()
    humidity = models.IntegerField()

    def __str__(self):
        return self.city_name


from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    founded_year = models.DateField()

    def __str__(self):
        return self.name

class Car(models.Model):
    car_name = models.CharField(max_length=200)
    car_year = models.DateField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='cars')

    def __str__(self):
        return self.car_name

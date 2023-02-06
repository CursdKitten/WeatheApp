from django.db import models
from django.utils import timezone

# Create your models here.

class Weather(models.Model):
    date_created_at = models.DateTimeField(null=False, default=timezone.now)
    address =  models.CharField(max_length=100, null=True)
    temperature = models.FloatField(null=True)
    symbol = models.CharField(max_length=10, null=True)
    description = models.CharField(max_length=50, null=True)
    feels_like = models.FloatField(null=True)

class APIKey(models.Model):
    name = models.CharField(max_length=50, null=True)
    key = models.CharField(max_length=100, null=True)


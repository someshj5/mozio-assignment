from django.db import models
from django.conf import settings
# Create your models here.



class Polygon(models.Model):
	email = models.CharField(max_length = 100)
	price = models.FloatField()
	provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    


class PolygonCoordinates(models.Model):
    latitude = models.DecimalField(max_digits=9,decimal_places=6)
    longitude = models.DecimalField(max_digits=9,decimal_places=6)
    Polygon = models.ForeignKey(Polygon, on_delete=models.CASCADE)


from django.db import models

# Create your models here.
class loldata(models.Model):

    hero = models.CharField(max_length=32)
    level =models.IntegerField()
    role = models.CharField(max_length=32)
    win = models.FloatField()
    pick = models.FloatField()
    ban = models.FloatField()
    tier = models.CharField(max_length=32)


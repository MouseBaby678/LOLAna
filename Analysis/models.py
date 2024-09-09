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

class hero_statistics(models.Model):

    hero = models.CharField(max_length=32)
    games_played = models.IntegerField()
    kda = models.FloatField()
    cs = models.FloatField()#补刀数
    gold = models.FloatField()
    win = models.FloatField()
    pick = models.FloatField()
    ban = models.FloatField()
    queue_type = models.CharField(max_length=32)
    tier = models.CharField(max_length=32)
    region = models.CharField(max_length=32)

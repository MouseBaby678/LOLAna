# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from Analysis import models


# class OpggspiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     hero = scrapy.Field()
#     tier = scrapy.Field()
#     role = scrapy.Field()
#     win = scrapy.Field()
#     pick = scrapy.Field()
#     ban = scrapy.Field()
#     pass
class loldataItem(DjangoItem):
    django_model = models.loldata
class hero_statisticsItem(DjangoItem):
    django_model = models.hero_statistics
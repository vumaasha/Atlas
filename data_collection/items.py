# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()


class FlipkartItem(scrapy.Item):
    # define the fields for your item here like:
    image_urls = scrapy.Field()
    page_url = scrapy.Field()
    image_paths = scrapy.Field()


class UtsavFashionItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    image_name = scrapy.Field()
    image_path = scrapy.Field()

class CraftsvillaItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    image_name = scrapy.Field()
    image_path = scrapy.Field()

class MirrawItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    image_name = scrapy.Field()
    image_path = scrapy.Field()


class IndianClothStoreItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    image_name = scrapy.Field()
    image_path = scrapy.Field()


class IndiaRushItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    image_name = scrapy.Field()
    image_path = scrapy.Field()

class IndiaEmporiumItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    image_name = scrapy.Field()
    image_path = scrapy.Field()

class BollywoodKartItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    image_name = scrapy.Field()
    image_path = scrapy.Field()

class ZipkerItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    image_name = scrapy.Field()
    image_path = scrapy.Field()

class SnapdealItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    image_name = scrapy.Field()
    image_path = scrapy.Field()

class VoonikItem(scrapy.Item):
    # define the fields for your item here like:
    image_url = scrapy.Field()
    image_name = scrapy.Field()
    image_path = scrapy.Field()
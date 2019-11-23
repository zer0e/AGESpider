# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AgeprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    region = scrapy.Field()
    anime_type = scrapy.Field()
    original_name = scrapy.Field()
    other_name = scrapy.Field()
    chinese_name = scrapy.Field()
    detail = scrapy.Field()
    author = scrapy.Field()
    company = scrapy.Field()
    time = scrapy.Field()
    status = scrapy.Field()
    plot_type = scrapy.Field()
    tag = scrapy.Field()
    website = scrapy.Field()
    download_site1 = scrapy.Field()
    download_site2 = scrapy.Field()
    pwd1 = scrapy.Field()
    pwd2 = scrapy.Field()
    pass

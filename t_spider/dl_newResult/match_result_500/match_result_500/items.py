# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MatchResult500Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    changci = scrapy.Field()
    match_date = scrapy.Field()
    goalline = scrapy.Field()
    first_half = scrapy.Field()
    whole = scrapy.Field()

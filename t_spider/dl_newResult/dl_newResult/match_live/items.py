# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MatchLiveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    league_id = scrapy.Field()
    first_half = scrapy.Field()
    whole = scrapy.Field()
    status = scrapy.Field()
    minute = scrapy.Field()
    goalline = scrapy.Field()
    match_time = scrapy.Field()

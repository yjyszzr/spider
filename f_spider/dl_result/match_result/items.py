# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MatchResultItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    changci_id = scrapy.Field()
    play_type = scrapy.Field()
    cell_name = scrapy.Field()
    goalline = scrapy.Field()
    single = scrapy.Field()
    odds = scrapy.Field()
    play_code = scrapy.Field()
    cell_code = scrapy.Field()

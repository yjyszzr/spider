# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DlSeasonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    season_id = scrapy.Field()
    season = scrapy.Field()
    league_name = scrapy.Field()

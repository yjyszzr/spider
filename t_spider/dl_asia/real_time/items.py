# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RealTimeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    real_odds1 = scrapy.Field()
    real_rule = scrapy.Field()
    real_odds2 = scrapy.Field()
    odds1_change = scrapy.Field()
    odds2_change = scrapy.Field()
    time_minus = scrapy.Field()
    ratio_h = scrapy.Field()
    ratio_a = scrapy.Field()
    index_h = scrapy.Field()
    index_a = scrapy.Field()
    asia_id = scrapy.Field()
    changci_id = scrapy.Field()
    com_name = scrapy.Field()
    init_odds1 = scrapy.Field()
    init_rule = scrapy.Field()
    init_odds2 = scrapy.Field()


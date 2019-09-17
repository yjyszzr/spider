# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DlAsianCupGjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jc_id = scrapy.Field()
    p_id = scrapy.Field()
    name = scrapy.Field()
    odds_type = scrapy.Field()
    rank_id = scrapy.Field()
    contry_name = scrapy.Field()
    prizes = scrapy.Field()
    pr = scrapy.Field()
    status = scrapy.Field()
    pic = scrapy.Field()

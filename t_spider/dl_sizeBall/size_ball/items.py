# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SizeBallItem(scrapy.Item):
    # define the fields for your item here like:
    #赔率公司
    name = scrapy.Field()
    #即时大
    timely_big = scrapy.Field()
    #即时盘
    timely_dish = scrapy.Field()
    #即时小
    timely_small = scrapy.Field()
    # 即时变化时间
    timely_time = scrapy.Field()
    #初始大
    init_big = scrapy.Field()
    #初始盘
    init_dish = scrapy.Field()
    #初始小
    init_small = scrapy.Field()
    # 初始变化时间
    init_time = scrapy.Field()
    #500w场次id
    id = scrapy.Field()
    #竞彩网场次id
    changci_id = scrapy.Field()



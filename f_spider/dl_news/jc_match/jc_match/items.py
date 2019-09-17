# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JcMatchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #发布日期
    date = scrapy.Field()
    #内容
    data = scrapy.Field()
    #标题
    title = scrapy.Field()
    #来源
    ref = scrapy.Field()
    #来源于哪个分类
    extend_cat = scrapy.Field()

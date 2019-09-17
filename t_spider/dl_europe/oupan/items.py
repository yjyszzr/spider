# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OupanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    changci_id = scrapy.Field()
    real_win = scrapy.Field()
    real_draw = scrapy.Field()
    real_lose = scrapy.Field()
    time_minus = scrapy.Field()
    win_ratio = scrapy.Field()
    draw_ratio = scrapy.Field()
    lose_ratio = scrapy.Field()
    per = scrapy.Field()
    win_index = scrapy.Field()
    draw_index = scrapy.Field()
    lose_index = scrapy.Field()
    europe_id = scrapy.Field()
    com_name = scrapy.Field()
    order_num = scrapy.Field()
    init_win = scrapy.Field()
    init_draw = scrapy.Field()
    init_lose = scrapy.Field()
    win_change = scrapy.Field()
    draw_change = scrapy.Field()
    lose_change = scrapy.Field()

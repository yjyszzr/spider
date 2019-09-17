# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DlMatchSupportItem(scrapy.Item):
    # define the fields for your item here like:
    support_id = scrapy.Field()
    changci_id = scrapy.Field()
    win_num = scrapy.Field()
    lose_num = scrapy.Field()
    draw_num = scrapy.Field()
    pre_win = scrapy.Field()
    pre_lose = scrapy.Field()
    pre_draw = scrapy.Field()
    total = scrapy.Field()
    play_type = scrapy.Field()

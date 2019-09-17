# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DlResultBkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #胜负比分
    mnl_score = scrapy.Field()
    #胜负彩果
    mnl_result = scrapy.Field()
    #让分胜负让分
    hdc_let = scrapy.Field()
    #让分胜负彩果
    hdc_result = scrapy.Field()
    #胜分差彩果
    wnm_result = scrapy.Field()
    #大小分预设总分
    hilo_score = scrapy.Field()
    #大小分彩果
    hilo_result = scrapy.Field()
    #赛事编号
    match_num = scrapy.Field()
    #比赛时间
    match_time = scrapy.Field()
    league_from = scrapy.Field()

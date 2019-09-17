# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DlScore5Item(scrapy.Item):
    #排名
    order = scrapy.Field()
    #联赛id
    l_id = scrapy.Field()
    #类型
    type = scrapy.Field()
    #球队名
    team_name = scrapy.Field()
    #赛场次数
    match_num = scrapy.Field()
    #胜场次数
    match_h = scrapy.Field()
    #平场次数
    match_d = scrapy.Field()
    #负场次数
    match_a = scrapy.Field()
    #进球数
    ball_in = scrapy.Field()
    # 失球数
    ball_lose = scrapy.Field()
    #积分
    score = scrapy.Field()
    team_id = scrapy.Field()
    season_id = scrapy.Field()

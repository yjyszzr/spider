# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeamPlayer500Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #球队id
    team_id = scrapy.Field()
    #球员id
    player_id = scrapy.Field()
    #球员名字
    player_name = scrapy.Field()
    #生日
    birthday = scrapy.Field()
    #球衣号码
    player_num = scrapy.Field()
    #球员位置
    player_type = scrapy.Field()
    #年龄
    age = scrapy.Field()
    #国籍
    contry = scrapy.Field()
    #球员身价
    player_price = scrapy.Field()
    #身高
    height = scrapy.Field()
    #体重
    weight = scrapy.Field()


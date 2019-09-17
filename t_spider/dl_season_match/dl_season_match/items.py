# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DlSeasonMatchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    match_time = scrapy.Field()
    home_team_id = scrapy.Field()
    home_team = scrapy.Field()
    visitor_team_id = scrapy.Field()
    visitor_team = scrapy.Field()
    match_score = scrapy.Field()
    match_group_id = scrapy.Field()
    group_name = scrapy.Field()


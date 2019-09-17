# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DlTeamAll5Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    league_name = scrapy.Field()
    match_time = scrapy.Field()
    home_team = scrapy.Field()
    score = scrapy.Field()
    visiting_team = scrapy.Field()
    result = scrapy.Field()
    team_id =scrapy.Field()
    h_id =scrapy.Field()
    v_id =scrapy.Field()

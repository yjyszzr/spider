# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeamPicItem(scrapy.Item):
    # define the fields for your item here like:
    team_id = scrapy.Field()
    team_pic = scrapy.Field()
    image_url = scrapy.Field()
    sporttery_teamid = scrapy.Field()
    team_name = scrapy.Field()
    team_addr = scrapy.Field()
    team_type = scrapy.Field()

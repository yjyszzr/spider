# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DlShooterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    player_name = scrapy.Field()
    team_name = scrapy.Field()
    play_num = scrapy.Field()
    season_id = scrapy.Field()
    id = scrapy.Field()
    sort = scrapy.Field()



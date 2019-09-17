# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DlMatchNbaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    league_name = scrapy.Field()
    league_abbr = scrapy.Field()
    changci_id = scrapy.Field()
    changci = scrapy.Field()
    home_team_id = scrapy.Field()
    home_team_name = scrapy.Field()
    home_team_abbr = scrapy.Field()
    home_team_rank = scrapy.Field()
    visiting_team_id = scrapy.Field()
    visiting_team_name = scrapy.Field()
    visiting_team_abbr = scrapy.Field()
    visiting_team_rank = scrapy.Field()
    match_time = scrapy.Field()
    show_time = scrapy.Field()
    is_show = scrapy.Field()
    match_sn = scrapy.Field()
    play_content = scrapy.Field()
    play_type = scrapy.Field()

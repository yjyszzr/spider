# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dl_season.items import DlSeasonItem
import re

class SeasonSpider(CrawlSpider):
    name = 'season'
    allowed_domains = ['500.com']
    start_urls = ['http://liansai.500.com/']

    rules = (
        Rule(LinkExtractor(allow=r'zuqiu-\d+/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        try:
            item = DlSeasonItem()
            item['season_id'] = int(re.search('zuqiu-(\d+)',response.url).group(1))
            item['season'] = response.xpath('//span[@class="ldrop_tit_txt"]/text()').extract_first()
            item['league_name'] = response.xpath('//li[@class="on"]/a/text()').extract_first().replace('首页','')
            yield item
        except Exception as e:
            print("暂无数据{}".format(e))
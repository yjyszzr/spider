# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from dl_shooter.items import DlShooterItem


class ShooterSpider(CrawlSpider):
    name = 'shooter'
    allowed_domains = ['500.com']
    start_urls = ['http://liansai.500.com/']

    rules = (
        Rule(LinkExtractor(allow=r'zuqiu-\d+/'), callback='parse_item',follow=True),
    )

    def parse_item(self, response):

        try:
            nodes = response.xpath('//table[contains(@class,"lshesb_list_s")]//tr')
            j = 1
            for node in nodes:
                item = DlShooterItem()
                item['player_name'] = node.xpath('./td[1]/a/text()').extract_first()
                item['team_name'] = node.xpath('./td[2]/a/text()').extract_first()
                num = node.xpath('./td[3]/text()').extract_first()
                item['play_num'] = int(re.search('\d+',num).group())
                item['season_id'] = int(re.search('zuqiu-(\d+)',response.url).group(1))
                item['id'] = int(str(item['season_id'])+str(j))
                item['sort'] = j
                j += 1
                yield item
        except Exception as e:
            print("暂无数据{}".format(e))

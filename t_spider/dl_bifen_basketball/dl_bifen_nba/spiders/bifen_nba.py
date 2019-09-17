# -*- coding: utf-8 -*-
import scrapy
from dl_bifen_nba.items import DlBifenNbaItem
import re


class BifenNbaSpider(scrapy.Spider):
    name = 'bifen_nba'
    allowed_domains = ['500.com']
    start_urls = ['http://zx.500.com/jclq/kaijiang.php']
    # start_urls = ['http://zx.500.com/jclq/kaijiang.php?playid=0&ggid=0&d=2018-09-14']
    def parse(self, response):
        data = response.body.decode('gbk')
        node_list = re.findall('<td>(周.*?)</td>.*?class="eng">(\d+-\d+ \d+:\d+)</td>.*?class="eng">(\d+:\d+)</td>', data,re.S)
        if node_list:
            for changci, match_date,whole in node_list:
                item = DlBifenNbaItem()
                item['changci'] = changci
                item['match_date'] = match_date
                item['whole'] = whole
                yield item


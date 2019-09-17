# -*- coding: utf-8 -*-
import scrapy
import re
from pymysql import connect
from match_result_500.items import MatchResult500Item


class A500Spider(scrapy.Spider):
    name = 'a500'
    allowed_domains = ['500.com']
    start_urls = ['http://zx.500.com/jczq/kaijiang.php']

    def parse(self, response):

        data = response.body.decode('gbk')
        node_list = re.findall('<td>(周.*?)</td>.*?(\d+-\d+ \d+:\d+).*?(-\d+|\+\d+)</span>.*?class="eng">\((.*?)\).*?(\d+:\d+)</td>',data,re.S)

        for changci,match_date,goalline,first_half,whole in node_list:
            item = MatchResult500Item()
            item['changci'] = changci
            item['match_date'] = match_date
            item['goalline'] = goalline
            item['first_half'] = first_half
            item['whole'] = whole
            yield item



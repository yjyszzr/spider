# -*- coding: utf-8 -*-
import scrapy
import re
import time
import re
import lxml
from super_miss.items import SuperMissItem

class SuperSpider(scrapy.Spider):
    name = 'super'
    allowed_domains = ['500.com']
    #实时
    start_urls = ['http://datachart.500.com/dlt/']
    #历史
    # start_urls = ['http://datachart.500.com/dlt/zoushi/newinc/jbzs_foreback.php?expect=all&from=18027&to=18056']
    # start_urls = ['http://datachart.500.com/dlt/zoushi/newinc/jbzs_foreback.php?expect=100']
    def parse(self, response):
        res = response.body.decode('gbk')
        num = re.findall('align="center">(\d+)(.*?)</tr>',res,re.S)
        for i,j in num:
            n = 1
            html = lxml.etree.HTML(j)
            list = html.xpath('//td')
            #前区遗漏
            pre_drop = []
            #后区遗漏
            post_drop = []
            for node in list:
                item = SuperMissItem()
                flat = node.xpath('./@class')[0]
                if n <36:
                    if 'chartBall' in flat:
                        pre_drop.append('0')
                    else:
                        pre_drop.append(node.xpath('./text()')[0])
                else:
                    if 'chartBall' in flat:
                        post_drop.append('0')
                    else:
                        post_drop.append(node.xpath('./text()')[0])
                n += 1
            pre_drop = ','.join(pre_drop)
            post_drop = ','.join(post_drop)
            item['term_num'] = i
            item['pre_drop'] = pre_drop
            item['post_drop'] = post_drop
            yield item



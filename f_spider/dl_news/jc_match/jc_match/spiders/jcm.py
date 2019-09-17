# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time
from jc_match.items import JcMatchItem
import re

class JcmSpider(CrawlSpider):
    name = 'jcm'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://info.sporttery.cn/roll/fb_list.php?&s=fb&c[]=%BE%BA%B2%CA%C7%B0%D5%B0&c[]=%BE%BA%B2%CA%C9%CB%CD%A3&c[]=%BE%BA%B2%CA%D5%BD%B1%A8','http://info.sporttery.cn/roll/fb_list.php?&s=fb&c=%BE%BA%B2%CA%B3%A1%CD%E2','http://info.sporttery.cn/roll/fb_list.php?&s=fb&c=%BE%BA%B2%CA%CA%FD%BE%DD']

    rules = (

        #今日数据
        Rule(LinkExtractor(allow=r'football/.*?/{}/{}'.format(time.strftime("%Y"),time.strftime("%m%d"))),callback='parse_item'),
        #自定义数据
        # Rule(LinkExtractor(allow=r'football/.*?/2018/0626'),callback='parse_item'),
    )

    def parse_item(self, response):

        str = response.xpath('//p/text()').extract()

        #内容
        data = ''.join(str)
        str_data = re.sub('\s+','',data)
        #标题
        title = response.xpath('//h1/text()').extract_first()

        da = response.xpath('//div[@class="s-tit"]/text()').extract_first().split(' ')
        #来源网站
        ref = da[2].strip()
        #发布时间
        date_time =' '.join(da[0:2])

        item = JcMatchItem()
        item['data'] = str_data
        item['title'] = title
        item['ref'] = ref
        item['date'] = date_time

        #如果内容中有双引号则替换为单引号
        if '"' in item['data']:
            item['data'] = re.sub('"',"'",item['data'])
        extend_cat = re.search('football/(.*?)/',response.url).group(1)
        e = {
            "jczb":1,
            "jcqz":1,
            "jccw":2,
            "jcsj":3
        }
        item['extend_cat'] = e[extend_cat]
        yield item


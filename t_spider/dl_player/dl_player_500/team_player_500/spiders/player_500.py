# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from team_player_500.items import TeamPlayer500Item


class Player500Spider(CrawlSpider):
    name = 'player_500'
    allowed_domains = ['500.com']
    start_urls = ['http://liansai.500.com/']
    rules = (
        Rule(LinkExtractor(allow=r'/zuqiu-\d+/'),follow=True),
        Rule(LinkExtractor(allow=r'/team/\d+/'),follow=True),
        Rule(LinkExtractor(allow=r'/player/\d+-\d+/'),callback='parse_item'),
    )
    def parse_item(self, response):
        item = TeamPlayer500Item()
        pos = {
            '门将': 0,
            '后卫': 1,
            '中场': 2,
            '前锋': 3,
        }
        item['team_id'] = int(re.search('/player/(\d+)-\d+/', response.url).group(1))
        item['player_id'] = int(re.search('/player/\d+-(\d+)/', response.url).group(1))
        item['player_name'] = response.xpath("//div[@class='itm_name']/text()").extract_first()
        try:
            item['birthday'] = response.xpath("//div[@class='itm_bd']/table//tr[2]/td[1]/text()").extract_first()
            item['birthday'] = re.search('\d+-\d+-\d+', item['birthday']).group()
            item['age'] = int(
                response.xpath("//div[@class='itm_bd']//tr[1]/td[1]/text()").extract_first().replace('年龄：', '').replace(
                    '岁',
                    ''))
        except:
            item['birthday'] = ''
            item['age'] = 0
        item['contry'] = response.xpath("//div[@class='itm_bd']//tr[1]/td[2]/text()").extract_first().replace('国籍：', '')
        item['player_price'] = response.xpath("//div[@class='itm_bd']//tr[1]/td[3]/text()").extract_first().replace(
            '球员身价：', '')
        item['height'] = response.xpath("//div[@class='itm_bd']//tr[3]/td[1]/text()").extract_first().replace('身高：', '')
        try:
            item['player_type'] = response.xpath("//div[@class='itm_bd']//tr[3]/td[2]/text()").extract_first().replace(
                '位置：', '')
            item['player_type'] = pos[item['player_type']]
        except:
            item['player_type'] = 4
        item['weight'] = response.xpath("//div[@class='itm_bd']//tr[4]/td[1]/text()").extract_first().replace('体重：', '')
        try:
            item['player_num'] = int(
                response.xpath("//div[@class='itm_bd']//tr[4]/td[2]/text()").extract_first().replace('球衣号码：', '').replace(
                    '号', ''))
        except:
            item['player_num'] = 0
        yield item

# -*- coding: utf-8 -*-
import scrapy
import re
from size_ball.items import SizeBallItem
from pymysql import connect

class SizeSpider(scrapy.Spider):
    name = 'size'
    allowed_domains = ['500.com']
    start_urls = ['http://live.500.com']

    def parse(self, response):
        res = response.body.decode('gbk')
        id_list = re.findall('//odds.500.com/fenxi/shuju-(\d+).shtml',res)
        for id in id_list:
            url = "http://odds.500.com/fenxi/daxiao-{}.shtml".format(id)
            yield scrapy.Request(url=url,meta={'id':id},callback=self.parse_item)

    def parse_item(self,response):
        node_list = response.xpath('//tr')
        id = response.meta['id']
        db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X',
                     database='cxm_lottery', charset='utf8')
        cur = db.cursor()
        match_time = response.xpath('//p[@class="game_time"]/text()').extract_first().replace('比赛时间', '')
        home_name = response.xpath('//title/text()').extract_first().split('VS')[0]
        sql = "select changci_id from dl_match where match_time='{}' and home_team_name='{}';".format(match_time,home_name)
        cur.execute(sql)
        #竞彩网场次ID
        changci_id = cur.fetchone()[0]
        for node in node_list:
            item = SizeBallItem()
            item['name'] = node.xpath('./td[2]/p/a/@title').extract_first()
            if item['name']:
                # 场次ID
                item['id'] = id
                # 即时大
                item['timely_big'] = node.xpath('./td[3]//tr/td[1]/text()').extract_first()
                # 即时盘
                item['timely_dish'] = node.xpath('./td[3]//tr/td[2]/text()').extract_first()
                # 即时小
                item['timely_small'] = node.xpath('./td[3]//tr/td[3]/text()').extract_first()
                # 即时变化时间
                item['timely_time'] = node.xpath('./td[4]/time/text()').extract_first()
                # 初始大
                item['init_big'] = node.xpath('./td[5]//tr/td[1]/text()').extract_first()
                # 初始盘
                item['init_dish'] = node.xpath('./td[5]//tr/td[2]/text()').extract_first()
                # 初始小
                item['init_small'] = node.xpath('./td[5]//tr/td[3]/text()').extract_first()
                # 初始变化时间
                item['init_time'] = node.xpath('./td[6]/time/text()').extract_first()
                item['changci_id'] = changci_id
                yield item
        cur.close()
        db.close()


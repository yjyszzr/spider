# -*- coding: utf-8 -*-
import scrapy
from pymysql import connect
from dl_future_5.items import DlFuture5Item

class FutureSpider(scrapy.Spider):
    name = 'future'
    allowed_domains = ['500.com']
    def start_requests(self):
        db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',
                     charset='utf8')
        cur = db.cursor()
        cur.execute("select team_id from dl_team_500w")
        ids = cur.fetchall()
        cur.close()
        db.close()
        for i in ids:
            team_id = i[0]
            url = "http://liansai.500.com/team/{}/teamfixture/".format(team_id)
            yield scrapy.Request(url=url,meta={'team_id':team_id})

    def parse(self, response):
        nodes = response.xpath('//*[@id="f_table"]/tr')
        for node in nodes:
            item = DlFuture5Item()
            item['team_id'] = response.meta['team_id']
            item['league_name'] = node.xpath('./td[1]/a/text()').extract_first()
            item['match_time'] = node.xpath('./td[2]/text()').extract_first().strip()
            item['home_team'] = node.xpath('./td[3]/a/text()').extract_first()
            item['visiting_team'] = node.xpath('./td[5]/a/text()').extract_first()
            yield item


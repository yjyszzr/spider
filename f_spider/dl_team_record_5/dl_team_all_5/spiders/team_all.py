# -*- coding: utf-8 -*-
import scrapy
from pymysql import connect
from dl_team_all_5.items import DlTeamAll5Item
import json
import re

class TeamAllSpider(scrapy.Spider):
    name = 'team_record'
    allowed_domains = ['500.com']
    def start_requests(self):
        db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',charset='utf8')
        cur = db.cursor()
        cur.execute("select team_id from dl_team_500w")
        ids = cur.fetchall()
        cur.close()
        db.close()
        for i in ids:
            team_id = i[0]
            url = "http://liansai.500.com/index.php?c=teams&a=ajax_fixture&hoa=0&records=10&tid={}".format(team_id)
            yield scrapy.Request(url=url,meta={'team_id':team_id})
    def parse(self, response):
        res = response.body.decode()
        team_id = response.meta['team_id']
        ds = json.loads(res)['list']
        for d in ds:
            item = DlTeamAll5Item()
            item['league_name'] = d['SIMPLEGBNAME']
            item['match_time'] = d['MATCHDATE']
            item['home_team'] = d['HOMETEAMSXNAME']
            item['h_id'] = d['HOMETEAMID']
            item['v_id'] = d['AWAYTEAMID']
            item['score'] = d['HOMESCORE'] + ':' + d['AWAYSCORE']
            item['visiting_team'] = d['AWAYTEAMSXNAME']
            try:
                item['result'] = re.search('<span.*?>(.*?)</span>',d['RESULT']).group(1)
            except:
                item['result'] = '无'
            item['team_id'] = team_id
            print(item)
            yield item




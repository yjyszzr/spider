# -*- coding: utf-8 -*-
import scrapy
from pymysql import connect
import json
from dl_score_5.items import DlScore5Item
import requests

class Score5Spider(scrapy.Spider):
    name = 'score_5'
    allowed_domains = ['500.com']
    def start_requests(self):
        db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',
                     charset='utf8')
        cur = db.cursor()
        #杯赛
        cur.execute("select l_id from dl_league_500w where is_league=0")
        bs = cur.fetchall()
        #联赛
        cur.execute("select l_id from dl_league_500w where is_league=1")
        ls = cur.fetchall()
        cur.close()
        db.close()
        for l in ls:
            l_id = l[0]
            for i in ["all","home","away"]:
                url = "https://ews.500.com/library/zq/integrate?&leagueid={}&iscup=0&vtype={}".format(l_id,i)
                yield scrapy.Request(url=url,meta={'type':i,'l_id':l_id})
        for b in bs:
            l_id = b[0]
            ul = "https://ews.500.com/library/zq/integrate?&leagueid={}&iscup=1&vtype=all".format(l_id)
            yield scrapy.Request(url=ul,meta={'l_id':l_id},callback=self.parse_it)
    def parse(self, response):
        try:
            res = response.body.decode()
            ty = response.meta['type']
            l_id = response.meta['l_id']
            val = json.loads(res)['data']['values']
            r = requests.get(url="https://ews.500.com/library/zq/baseinfo?leagueid={}".format(l_id)).content.decode()
            season_id = json.loads(r)['data']['seasonid']
            for v in val:
                item = DlScore5Item()
                item['order'] = v['order']
                item['l_id'] = l_id
                item['type'] = ty
                item['team_name'] = v['teamsxname']
                item['match_num'] = v['total']
                item['match_h'] = v['win']
                item['match_d'] = v['draw']
                item['match_a'] = v['lost']
                item['ball_in'] = v['jq']
                item['ball_lose'] = v['sq']
                item['score'] = v['score']
                item['team_id'] = v['teamid']
                item['season_id'] = int(season_id)
                yield item
        except Exception as e:
            print("联赛错误信息>>{}".format(e))
    def parse_it(self,response):
        try:
            res = response.body.decode()
            l_id = response.meta['l_id']
            r = requests.get(url="https://ews.500.com/library/zq/baseinfo?leagueid={}".format(l_id)).content.decode()
            season_id = json.loads(r)['data']['seasonid']
            sort = json.loads(res)['data']['sort']
            val = json.loads(res)['data']['values']
            for ty in sort:
                for v in val[ty]:
                    item = DlScore5Item()
                    item['order'] = v['order']
                    item['l_id'] = l_id
                    item['type'] = ty.replace('组','')
                    item['team_name'] = v['teamsxname']
                    item['match_num'] = v['total']
                    item['match_h'] = v['win']
                    item['match_d'] = v['draw']
                    item['match_a'] = v['lost']
                    item['ball_in'] = v['jq']
                    item['ball_lose'] = v['sq']
                    item['score'] = v['score']
                    item['team_id'] = v['teamid']
                    item['season_id'] = int(season_id)
                    yield item
        except Exception as e:
            print("杯赛错误信息>>{}".format(e))



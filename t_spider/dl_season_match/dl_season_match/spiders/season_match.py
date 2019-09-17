# -*- coding: utf-8 -*-
import scrapy
from pymysql import connect
import json
from dl_season_match.items import DlSeasonMatchItem
import requests
import json
import time

class SeasonMatchSpider(scrapy.Spider):
    name = 'season_match'
    allowed_domains = ['500.com']
    # start_urls = ['https://ews.500.com/library/zq/switch?&stageid=13378&switchid=4837&roundtype=other']
    def start_requests(self):
        db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',
                     charset='utf8')
        cur = db.cursor()
        cur.execute("select stageid,switchid,match_group_id from dl_season_group_500w")
        ids = cur.fetchall()
        for stageid,switchid,match_group_id in ids:
            time.sleep(1)
            url = "https://ews.500.com/library/zq/switch?&stageid={}&switchid={}&roundtype=round".format(stageid,switchid)
            res = requests.get(url=url).content.decode()
            d = json.loads(res)['data']

            if d:
                yield scrapy.Request(url=url,meta={"match_group_id":match_group_id})
            else:
                url = "https://ews.500.com/library/zq/switch?&stageid={}&switchid={}&roundtype=other".format(stageid,switchid)
                yield scrapy.Request(url=url, meta={"match_group_id": match_group_id},callback=self.parse_it)
    def parse(self, response):

        try:
            match_group_id = response.meta['match_group_id']
            val = json.loads(response.body.decode())['data']['values']
            for i in val:
                item = DlSeasonMatchItem()
                item['match_group_id'] = match_group_id
                item['match_time'] = i['matchtime']
                item['home_team_id'] = int(i['homeid'])
                item['home_team'] = i['homesxname']
                item['visitor_team_id'] = int(i['awayid'])
                item['visitor_team'] = i['awaysxname']
                try:
                    item['match_score'] = i['homescore'] + ':' + i['awayscore']
                except:
                    item['match_score'] = 'vs'
                item['group_name'] = ''
                yield item
        except Exception as e:
            print(e, match_group_id)
    def parse_it(self,response):
        try:
            match_group_id = response.meta['match_group_id']
            v = json.loads(response.body.decode())['data']['values']
            for group_name, j in v.items():

                for data in j:
                    item = DlSeasonMatchItem()
                    item['match_group_id'] = match_group_id
                    item['match_time'] = data['matchtime']
                    item['home_team_id'] = int(data['homeid'])
                    item['home_team'] = data['homesxname']
                    item['visitor_team_id'] = int(data['awayid'])
                    item['visitor_team'] = data['awaysxname']
                    item['group_name'] = group_name
                    try:
                        item['match_score'] = data['homescore'] + ':' + data['awayscore']
                    except:
                        item['match_score'] = 'vs'
                    yield item
        except Exception as e:
            print(e, match_group_id)


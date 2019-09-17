# -*- coding: utf-8 -*-
import scrapy
import json
import re
from match_live.items import MatchLiveItem

class LiveSpider(scrapy.Spider):
    name = 'newresult'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://i.sporttery.cn/api/match_live_2/get_match_list']
    #http://i.sporttery.cn/api/match_live_2/get_match_updated

    def parse(self, response):
        data = response.body.decode()#[17:-2]
        dicts = re.findall('\{"m_id".*?\}',data)
        for i in dicts:
            dict = json.loads(i)
            item = MatchLiveItem()
            item['league_id'] = dict['m_id']
            item['minute'] = dict['minute']
            item['goalline'] = dict['goalline']
            item['match_time'] = dict['date_cn'] + ' ' + dict['time_cn']
            t = dict['minute']
            s = {
                "Fixture":'0',#未开赛
                "Played":'1',#已完成
                "Playing":'6',#进行中
                 "Postponed":'4',#推迟
                 "Suspended":'5',#暂停
                 "Cancelled":'2', #取消

            }

            if dict['status'] not in s:
                item['status'] = '0'
            else:
                item['status'] = s[dict['status']]

            #进行中
            if t:
                t = int(t)
                #比赛完成
                if t > 150:
                    item['status'] = '1'
            item['first_half'] = dict['hts_h'] + ':' + dict['hts_a']
            item['whole'] = dict['fs_h'] + ':' + dict['fs_a']
            yield item



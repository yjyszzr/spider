# -*- coding: utf-8 -*-
import scrapy
import json
import time
from dl_match_support.items import DlMatchSupportItem


class SupSpider(scrapy.Spider):
    name = 'sup'
    allowed_domains = ['sporttery.cn']
    start_urls = ['http://i.sporttery.cn/odds_calculator/get_proportion?i_format=json']

    def parse(self, response):
        res = response.body.decode()
        dict_data = json.loads(res)['data']
        for key,val in dict_data.items():
            for k,v in val.items():
                item = DlMatchSupportItem()
                if v['type'] == 'hhad':
                    v['type'] = 1
                else:
                    v['type'] = 2
                item['support_id']= v['id']
                item['changci_id']= v['mid']
                item['win_num']= v['win']
                item['lose_num']= v['lose']
                item['draw_num']= v['draw']
                item['pre_win']= v['pre_win']
                item['pre_lose']= v['pre_lose']
                item['pre_draw']= v['pre_draw']
                item['total']= v['total']
                item['play_type']= v['type']
                yield item



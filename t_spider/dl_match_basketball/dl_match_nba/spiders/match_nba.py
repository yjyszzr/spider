# -*- coding: utf-8 -*-
import scrapy
import json
import re
from dl_match_nba.items import DlMatchNbaItem
import datetime



# 合成match_cn所需要的字段
def em(str):
    try:
        da = re.sub('\d+','',str)
        n = re.search('\d+',str).group()
        if da == "周一":
            da = '1'
        elif da == '周二':
            da = '2'
        elif da == '周三':
            da = '3'
        elif da == '周四':
            da = '4'
        elif da == '周五':
            da = '5'
        elif da == '周六':
            da = '6'
        else:
            da = '7'
        num = da + n
        return num
    except:
        return None

class MatchNbaSpider(scrapy.Spider):
    name = 'match_nba'
    allowed_domains = ['sporttery.cn']
    def start_requests(self):
        ty = ['mnl','hdc','wnm','hilo']
        for t in ty:
            url = 'http://i.sporttery.cn/odds_calculator/get_odds?i_format=json&poolcode[]='+t
            yield scrapy.Request(url,meta={"type":t})

    def parse(self, response):
        men = {"mnl":2,
               "hdc":1,
               "wnm":3,
               "hilo":4,
               }
        ty = response.meta['type']
        res = response.body.decode('unicode-escape')
        data_dict = json.loads(res)['data']

        for k,v in data_dict.items():
            item = DlMatchNbaItem()
            try:
                v['h_order'] = re.search('\[.*?(\d+)\]',v['h_order']).group(1)
            except:
                v['h_order'] = ''
            try:
                v['a_order'] = re.search('\[.*?(\d+)\]',v['a_order']).group(1)
            except:
                v['a_order'] = ''
            item['league_name'] = v['l_cn']
            item['league_abbr']= v['l_cn_abbr']
            item['changci_id']= v['id']
            item['changci']= v['num']
            item['home_team_id']= v['h_id']
            item['home_team_name']= v['h_cn']
            item['home_team_abbr']= v['h_cn_abbr']
            item['home_team_rank']= v['h_order']
            item['visiting_team_id']= v['a_id']
            item['visiting_team_name']= v['a_cn']
            item['visiting_team_abbr']= v['a_cn_abbr']
            item['visiting_team_rank']= v['a_order']
            d1 = v['date']+' '+v['time']
            d2 = v['b_date']+' '+"00:00:00"
            item['match_time']= datetime.datetime.strptime(d1,"%Y-%m-%d %H:%M:%S")
            item['show_time']= datetime.datetime.strptime(d2,"%Y-%m-%d %H:%M:%S")

            item['is_show']= v['show']
            if em(v['num']):
                item['match_sn']= v['b_date'].replace('-','')+ em(v['num'])
            else:
                item['match_sn'] = None
            item['play_content']= v[ty]
            item['play_type'] = men[ty]

            yield item


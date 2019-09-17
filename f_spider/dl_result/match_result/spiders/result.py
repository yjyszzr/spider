# -*- coding: utf-8 -*-
import scrapy
from pymysql import connect
from match_result.items import MatchResultItem
import json
import time
import re

class ResultSpider(scrapy.Spider):
    name = 'result'
    allowed_domains = ['sporttery.cn']
    def start_requests(self):
        db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',
                     charset='utf8')
        cur = db.cursor()
        sql = "select changci_id,match_sn from dl_match where status = 1 and DATEDIFF(match_time,NOW()) > -3 and is_show=1;"
        cur.execute(sql)
        datas = cur.fetchall()
        cur.close()
        db.close()
        for changci_id,play_code in datas:

            url = "http://i.sporttery.cn/api/fb_match_info/get_pool_rs/?mid=" + str(changci_id)
            yield scrapy.Request(url=url,meta={"play_code":play_code,"changci_id":changci_id})
    def parse(self, response):
        changci_id = response.meta['changci_id']
        play_code =response.meta['play_code']
        data = response.body.decode()
        json_data = json.loads(data)
        dict_data = json_data["result"]["pool_rs"]

        if dict_data:
            for key, val in dict_data.items():
                item = MatchResultItem()
                #五种玩法枚举
                ty = {"hhad":"1","had":"2","ttg":"4","hafu":"5","crs":"3"}
                # cell_code枚举
                ply = {'5:0':'50','负胜':'03','1:1':'11','1:3':'13','0:5':'05','3:3':'33','2:5':'25','0:2':'02','平其它':'99','负其它':'09','5:2':'52','4:0':'40','5:1':'51','4:1':'41','1:0':'10','0:3':'03','1:5':'15','3:1':'31','3:2':'32','平平':'11','4:2':'42','负负':'00','胜胜':'33','0:1':'01','2:0':'20','1:4':'14','负平':'01','2:3':'23','0:0':'00','2:4':'24','平负':'10','1:2':'12','胜负':'30','胜其它':'90','0:4':'04','平胜':'13','胜平':'31','2:1':'21','3:0':'30','2:2':'22',"胜":"3","负":"0","平":"1"}
                item['play_type'] = ty[key]
                item['cell_name'] = val['prs_name']
                item['goalline'] = val['goalline']
                item['single'] = val['single']
                item['odds'] = val['odds']
                item['changci_id'] = changci_id
                item['play_code'] = play_code
                if val['prs_name'] in ply:
                    item['cell_code'] = ply[val['prs_name']]
                elif val['prs_name'] =='胜其他':
                    item['cell_code'] = "90"
                elif val['prs_name'] =='负其他':
                    item['cell_code'] = "09"
                elif val['prs_name'] =='平其他':
                    item['cell_code'] = "99"
                else:
                    item['cell_code'] = val['prs_name']
                    if '+' in item['cell_code']:
                        item['cell_code']= re.sub('\+','',item['cell_code'])                        
                yield item




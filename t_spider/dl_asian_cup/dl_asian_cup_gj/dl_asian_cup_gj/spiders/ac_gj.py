# -*- coding: utf-8 -*-
import scrapy
import re
import json
from dl_asian_cup_gj.items import DlAsianCupGjItem

class AcGjSpider(scrapy.Spider):
    name = 'ac_gj'
    allowed_domains = ['http://i.sporttery.cn']
    start_urls = ['http://i.sporttery.cn/rank_calculator/get_list?pcode[]=chp&i_callback=showChpList']

    def parse(self, response):
        try:
            data = response.body.decode('gbk')
            data = re.search('showChpList\((.*?)\);',data).group(1)
            data = json.loads(data)
            dict_data = data['data'][0]
            datas = dict_data['data']
            ls = re.findall('(\d+)-(.*?)-(.*?)-(.*?)-.*?-(.*?)-\d+-.*?-\d+-\d+-\d+-(.*?\.png)',datas)
            for rank_id,contry_name,status,prizes,pr,pic in ls:
                try:
                    item = DlAsianCupGjItem()
                    item['jc_id'] = dict_data['id']
                    item['p_id'] = dict_data['p_id']
                    item['name'] = dict_data['name']
                    item['odds_type'] = dict_data['odds_type']
                    item['rank_id'] = rank_id
                    item['contry_name'] = contry_name
                    item['prizes'] = prizes
                    item['pr'] = pr
                    if status == '开售':
                        item['status'] = 0
                    else:
                        item['status'] = 1
                    item['pic'] = pic
                    yield item
                except:
                    pass
        except:
            pass




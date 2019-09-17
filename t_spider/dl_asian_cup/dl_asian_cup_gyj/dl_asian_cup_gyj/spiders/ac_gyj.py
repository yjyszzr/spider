# -*- coding: utf-8 -*-
import scrapy
import re
import json
from dl_asian_cup_gyj.items import DlAsianCupGyjItem

class AcGyjSpider(scrapy.Spider):
    name = 'ac_gyj'
    allowed_domains = ['http://i.sporttery.cn']
    start_urls = ['http://i.sporttery.cn/rank_calculator/get_list?pcode[]=fnl&i_callback=showFnlList']

    def parse(self, response):

        try:

            data = response.body.decode('gbk')

            data = re.search('showFnlList\((.*?)\);',data).group(1)

            data = json.loads(data)
            dict_data = data['data'][0]
            datas = dict_data['data']

            ls = re.findall('(\d+)-(.*?)—(.*?)-(.*?)-(.*?)-.*?-(.*?)-\d+-.*?-\d+-\d+-\d+—\d+-(http.*?\.png)—(http.*?\.png)',datas)

            for num,contry_h,contry_v,status,prizes,odds,pic1,pic2 in ls:
                try:
                    # item = DlAsianCupGyjItem()
                    # item['jc_id'] = dict_data['id']
                    # item['p_id'] = dict_data['p_id']
                    # item['name'] = dict_data['name']
                    # item['odds_type'] = dict_data['odds_type']
                    # item['rank_id'] = rank_id
                    # item['contry_name'] = contry_name
                    # item['prizes'] = prizes
                    # item['pr'] = pr
                    # if status == '开售':
                    #     item['status'] = 0
                    # else:
                    #     item['status'] = 1
                    # item['pic'] = pic

                    # yield item
                    print(num,contry_h,contry_v,status,prizes,odds)
                except:
                    pass
        except:
            pass

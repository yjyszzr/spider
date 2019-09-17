# -*- coding: utf-8 -*-
import scrapy
from pymysql import connect
import json
from oupan.items import OupanItem

class OuSpider(scrapy.Spider):
    name = 'ou'
    allowed_domains = ['sporttery.cn']

    def start_requests(self):
        db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',
                     charset='utf8')
        cur = db.cursor()
        cur.execute(
            'select changci_id from dl_match where DATEDIFF(show_time,NOW()) >= 0 and is_del = 0 and is_show=1 and TIMESTAMPDIFF(MINUTE, match_time, NOW()) < 10')
        changci_ids = cur.fetchall()
        cur.close()
        db.close()
        for i in changci_ids:
            id = i[0]
            url = 'http://i.sporttery.cn/api/fb_match_info/get_europe/?f_callback=hb_odds&mid=' + str(id)
            yield scrapy.Request(url=url, meta={'id': id})
    def parse(self, response):
        res_data = response.body.decode()
        dict_data = json.loads(res_data[8:-2])
        data = dict_data['result']['data']
        for j in data:
            item = OupanItem()
            item['changci_id'] = response.meta['id']
            if j['win_change'] == 'up':
                j['win_change'] = 1
            elif j['win_change'] == 'down':
                j['win_change'] = 2
            else:
                j['win_change'] = 0

            if j['draw_change'] == 'up':
                j['draw_change'] = 1
            elif j['draw_change'] == 'down':
                j['draw_change'] = 2
            else:
                j['draw_change'] = 0

            if j['lose_change'] == 'up':
                j['lose_change'] = 1
            elif j['lose_change'] == 'down':
                j['lose_change'] = 2
            else:
                j['lose_change'] = 0
            item['real_win']=j['win']
            item['real_draw']=j['draw']
            item['real_lose']=j['lose']
            item['time_minus']=j['time_minus']
            item['win_ratio']=j['win_ratio']
            item['draw_ratio']= j['draw_ratio']
            item['lose_ratio']=j['lose_ratio']
            item['per'] = j['per']
            item['win_index']=j['win_index']
            item['draw_index']=j['draw_index']
            item['lose_index']=j['lose_index']
            item['com_name']=j['cn']
            item['order_num']=j['order']
            item['init_win']=j['win_s']
            item['init_draw']=j['draw_s']
            item['init_lose']=j['lose_s']
            item['win_change']=j['win_change']
            item['draw_change']=j['draw_change']
            item['lose_change']=j['lose_change']
            item['europe_id'] = j['id']

            yield item

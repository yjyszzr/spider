# -*- coding: utf-8 -*-
import scrapy
from pymysql import connect
import json
import time
from real_time.items import RealTimeItem

class RealSpider(scrapy.Spider):
    name = 'real_ya'
    allowed_domains = ['sporttery.cn']

    def start_requests(self):
        db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',
                     charset='utf8')
        cur = db.cursor()
        cur.execute('select changci_id from dl_match where DATEDIFF(show_time,NOW()) >= 0 and is_del = 0 and is_show=1 and TIMESTAMPDIFF(MINUTE, match_time, NOW()) < 10')
        changci_ids = cur.fetchall()
        cur.close()
        db.close()
        for i in changci_ids:
            id = i[0]
            url = 'http://i.sporttery.cn/api/fb_match_info/get_asia/?f_callback=asia_tb&mid=' + str(id)
            yield scrapy.Request(url=url,meta={'id':id})

    def parse(self, response):
        res_data = response.body.decode()
        dict_data = json.loads(res_data[8:-2])
        # 亚盘页面所有数据
        data = dict_data['result']['data']
        for j in data:
            item = RealTimeItem()
            item['changci_id'] = response.meta['id']
            if j['o1_change'] == 'up':
                j['o1_change'] = 1
            elif j['o1_change'] == 'down':
                j['o1_change'] = 2
            else:
                j['o1_change'] = 0

            if j['o2_change'] == 'up':
                j['o2_change'] = 1
            elif j['o2_change'] == 'down':
                j['o2_change'] = 2
            else:
                j['o2_change'] = 0
            item['real_odds1'] = j['o1']
            item['real_rule'] = j['o3']
            item['real_odds2'] = j['o2']
            item['odds1_change'] = j['o1_change']
            item['odds2_change'] = j['o2_change']
            item['time_minus'] = j['time_minus']
            item['ratio_h'] = j['o2_ratio']
            item['ratio_a'] = j['o1_ratio']
            item['index_h'] = j['o1_index']
            item['index_a'] = j['o2_index']
            item['asia_id'] = j['id']
            item['com_name'] = j['cn']
            item['init_odds1'] = j['o1_s']
            item['init_rule'] = j['o3_s']
            item['init_odds2'] = j['o2_s']
            # 判断数据中是否有该场次
            yield item



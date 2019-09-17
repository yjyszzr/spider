# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
import time

class MatchLivePipeline(object):

    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',
                     charset='utf8')
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.close()

    def process_item(self, item, spider):

        s = "select * from dl_match_result where changci_id={} and league_from = 0;".format(item['league_id'])
        desc = self.cur.execute(s)
        if desc:

            if item['status'] == '1' or item['status'] == '6':
                sql = "update dl_match_result set first_half='{}',whole='{}',match_status='{}',match_minutes='{}',goalline='{}',update_time={} where changci_id={} and status != '1';".format(item['first_half'], item['whole'], item['status'], item['minute'],item['goalline'],int(time.time()),item['league_id'])
                ts = '{}>>更新成功'.format(item['league_id'])
        else:


            sql = "insert into dl_match_result(changci_id,first_half,whole,match_status,match_minutes,goalline,create_time,update_time,match_time) values({},'{}','{}','{}','{}','{}',{},{},'{}');".format(item['league_id'],item['first_half'],item['whole'], item['status'],item['minute'],item['goalline'],int(time.time()),int(time.time()),item['match_time'])

            ts = '{}>>插入成功'.format(item['league_id'])
            print(sql)



        self.cur.execute(sql)
        self.db.commit()
        print(ts)

        return item

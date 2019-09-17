# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
import time

class MatchResultPipeline(object):
    def __init__(self):
        self.db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',
                     charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()

    def process_item(self, item, spider):
        desc = self.cur.execute("select * from dl_league_match_result where changci_id=%s and play_type=%s;"%(str(item['changci_id']),str(item['play_type'])))
        if desc:
            #更新
            sql  = "update dl_league_match_result set play_code='{}',cell_code='{}',cell_name='{}',goalline='{}',single={},odds={} where changci_id={} and play_type={};".format(item['play_code'],item['cell_code'],item['cell_name'],item['goalline'],item['single'],item['odds'],item['changci_id'],item['play_type'])
            self.cur.execute(sql)
            print("更新%d"%item['changci_id'])
        else:
            #插入
            sql = "insert into dl_league_match_result(play_type,cell_name,goalline,single,odds,changci_id,play_code,cell_code,create_time) values({},'{}','{}',{},{},{},'{}','{}',{});".format(item['play_type'],item['cell_name'],item['goalline'],item['single'],item['odds'],item['changci_id'],item['play_code'],item['cell_code'],int(time.time()))
            self.cur.execute(sql)
            print("插入%d"%item['changci_id'])
        self.db.commit()
        return item

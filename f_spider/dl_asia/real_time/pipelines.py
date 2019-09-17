# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
import time

class RealTimePipeline(object):
    def __init__(self):
        self.db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',
                     charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()
    
    def process_item(self, item, spider):
        
        desc = self.cur.execute("select * from dl_league_match_asia where changci_id ={} and asia_id={}".format(item['changci_id'],item['asia_id']))
        if desc:
            # 如果有则定期更新
            sql = "update dl_league_match_asia set real_odds1= {},real_rule = '{}',real_odds2 = {},odds1_change = {},odds2_change = {},time_minus = {},ratio_h = {},ratio_a = {} ,index_h =  {},index_a = {},update_time = {} where changci_id = {} and asia_id = {};".format(
                item['real_odds1'], item['real_rule'], item['real_odds2'], item['odds1_change'], item['odds2_change'],
                item['time_minus'], item['ratio_h'],
                item['ratio_a'], item['index_h'], item['index_a'], int(time.time()), item['changci_id'],
                item['asia_id'])
            self.cur.execute(sql)
            print("亚盘更新sql语句为:%s"%sql)

        else:
            # 如果没有则插入该数据
            sql = "INSERT INTO dl_league_match_asia(changci_id,asia_id,com_name,init_odds1,init_rule,init_odds2,real_odds1,real_rule,real_odds2,odds1_change,odds2_change,time_minus,ratio_h,ratio_a,index_h,index_a,create_time,update_time) VALUES ({},{},'{}',{},'{}',{},{},'{}',{},{},{},{},{},{},{},{},{},{});".format(
                item['changci_id'], item['asia_id'], item['com_name'], item['init_odds1'], item['init_rule'],
                item['init_odds2'], item['real_odds1'], item['real_rule'], item['real_odds2'],
                item['odds1_change'], item['odds2_change'], item['time_minus'], item['ratio_h'], item['ratio_a'], item['index_h'],
                item['index_a'], int(time.time()), int(time.time()))
            self.cur.execute(sql)
            print("亚盘插入sql语句为:%s"%sql)
        self.db.commit()
        return item

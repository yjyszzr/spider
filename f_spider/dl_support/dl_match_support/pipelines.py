# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
import time

class DlMatchSupportPipeline(object):
    def __init__(self):
        self.db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',
                     charset='utf8')
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):
        
        desc = self.cur.execute('select support_id from dl_match_support where support_id=%s;'%item['support_id'])
        if desc:
            #更新
            sql = "update dl_match_support set changci_id={},win_num={},lose_num={},draw_num={},pre_win='{}',pre_lose='{}',pre_draw='{}',total={},play_type={},update_time={} where support_id={};".format(item['changci_id'],item['win_num'],item['lose_num'],item['draw_num'],item['pre_win'],item['pre_lose'],item['pre_draw'],item['total'],item['play_type'],int(time.time()),item['support_id'])
            self.cur.execute(sql)
            print('更新%s成功>>>'%item['support_id'])
        else:
            #插入
            sql = "insert into dl_match_support(support_id,changci_id,win_num,lose_num,draw_num,pre_win,pre_lose,pre_draw,total,play_type,create_time,update_time) VALUES ({},{},{},{},{},'{}','{}','{}',{},{},{},{});".format(item['support_id'],item['changci_id'],item['win_num'],item['lose_num'],item['draw_num'],item['pre_win'],item['pre_lose'],item['pre_draw'],item['total'],item['play_type'],int(time.time()),int(time.time()),item['support_id'])
            self.cur.execute(sql)
            print('插入%s成功<<<'%item['support_id'])

        self.db.commit()
        return item

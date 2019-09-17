# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
from pymysql import connect

class OupanPipeline(object):

    def __init__(self):
        self.db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',
                     charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):
        des = self.cur.execute("select * from dl_league_match_europe where changci_id={} and europe_id={}".format(item['changci_id'],item['europe_id']))
        if des:
            # 更新
            sql = "update dl_league_match_europe set real_win= {},real_draw = {},real_lose = {},time_minus={},win_ratio='{}',draw_ratio='{}',lose_ratio='{}',per ='{}',win_index={},draw_index={},lose_index={},update_time={} where changci_id = {} and europe_id = {};".format(
                item['real_win'], item['real_draw'], item['real_lose'], item['time_minus'], item['win_ratio'],
                item['draw_ratio'],
                item['lose_ratio'], item['per'], item['win_index'], item['draw_index'], item['lose_index'],
                int(time.time()), item['changci_id'], item['europe_id'])
            self.cur.execute(sql)
            print("%s更新数据成功\n%s"%(time.ctime(),sql))
        else:
            sql = "INSERT INTO dl_league_match_europe(changci_id,europe_id,com_name,order_num,init_win,init_draw,init_lose,real_win,real_draw,real_lose,win_change,draw_change,lose_change,time_minus,win_ratio,draw_ratio,lose_ratio,per,win_index,draw_index,lose_index,create_time,update_time) VALUES ({},{},'{}',{},{},{},{},{},{},{},{},{},{},{},'{}','{}','{}','{}',{},{},{},{},{});".format(
                item['changci_id'], item['europe_id'], item['com_name'], item['order_num'], item['init_win'],
                item['init_draw'], item['init_lose'], item['real_win'], item['real_draw'],
                item['real_lose'], item['win_change'], item['draw_change'], item['lose_change'], item['time_minus'],
                item['win_ratio'],
                item['draw_ratio'], item['lose_ratio'], item['per'], item['win_index'], item['draw_index'],
                item['lose_index'], int(time.time()), int(time.time()))
            self.cur.execute(sql)
            print("%s插入数据成功\n%s"%(time.ctime(),sql))
        self.db.commit()
        return item

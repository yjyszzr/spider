# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
import time

class SizeBallPipeline(object):
    def __init__(self):
        self.db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):
        s = "select * from dl_league_match_daoxiao where changci_id={} and com_name='{}';".format(item['changci_id'],item['name'])
        desc = self.cur.execute(s)
        n = ''
        if desc:
            sql = "update dl_league_match_daoxiao set real_win='{}',real_draw='{}',real_lose='{}',real_time='{}',update_time={} where changci_id={} and com_name='{}';".format(item['timely_big'],item['timely_dish'],item['timely_small'],item['timely_time'],int(time.time()),item['changci_id'],item['name'])
            n = "更新:{}>成功!".format(item['changci_id'])
        else:
            sql = "insert into dl_league_match_daoxiao(changci_id,daoxiao_id,com_name,init_win,init_draw,init_lose,real_win,real_draw,real_lose,init_time,real_time,create_time,update_time) values({},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}',{},{});".format(item['changci_id'],item['id'],item['name'],item['init_big'],item['init_dish'],item['init_small'],item['timely_big'],item['timely_dish'],item['timely_small'],item['init_time'],item['timely_time'],int(time.time()),int(time.time()))
            n = "插入:{}>成功!".format(item['changci_id'])
        self.cur.execute(sql)
        self.db.commit()
        print(n)
        return item

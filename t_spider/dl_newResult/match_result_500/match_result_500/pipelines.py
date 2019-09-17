# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
import time
from datetime import datetime

class MatchResult500Pipeline(object):
    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):
        now = datetime.now()
        #表示今年
        year = now.strftime('%Y')
        #比赛时间
        match_time = year + '-' + item['match_date'] +':00'

        s = "select changci_id from dl_match where changci = '{}' and match_time like '%{}%';".format(item['changci'],item['match_date'])
        self.cur.execute(s)
        changci_id = self.cur.fetchone()[0]

        desc = self.cur.execute("select * from dl_match_result where changci_id = {} and league_from = 1;".format(changci_id))
        if desc:
            pass
        else:
            sql = "insert into dl_match_result(changci_id,first_half,whole,match_status,goalline,create_time,update_time,league_from,match_time) values({},'{}','{}','1','{}',{},{},1,'{}');".format(changci_id,item['first_half'],item['whole'],item['goalline'],int(time.time()),int(time.time()),match_time)

        self.cur.execute(sql)
        self.db.commit()
        print("插入>>{}成功!!".format(changci_id))
        return item

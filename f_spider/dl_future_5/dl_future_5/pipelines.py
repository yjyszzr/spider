# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
from datetime import datetime

class DlFuture5Pipeline(object):
    def __init__(self):
        self.db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):
        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')
        desc = self.cur.execute("select * from dl_team_future_500w where match_time='{}' and team_id={};".format(item['match_time'],item['team_id']))
        if desc:
            print('暂无更新')
        else:
            sql = "insert into dl_team_future_500w(match_time,league_abbr,home_abbr,visiting_abbr,team_id,create_time) values('{}','{}','{}','{}',{},'{}')".format(item['match_time'],item['league_name'],item['home_team'],item['visiting_team'],item['team_id'],now_time)
            self.cur.execute(sql)
            self.db.commit()
            print("插入{}成功!".format(item['team_id']))
        return item

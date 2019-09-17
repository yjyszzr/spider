# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
from datetime import datetime

class DlTeamAll5Pipeline(object):

    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.close()

    def process_item(self, item, spider):

        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')
        desc = self.cur.execute("select * from dl_team_record_500w where team_id={} and match_time ='{}';".format(item['team_id'],item['match_time']))

        if desc:
            sql = "update dl_team_record_500w set home_id={},visiting_id={},result='{}' where team_id={} and match_time ='{}';".format(item['h_id'],item['v_id'],item['result'],item['team_id'],item['match_time'])
            self.cur.execute(sql)
            self.db.commit()
            print("更新{}成功!".format(item['team_id']))
        else:
            sql = "insert into dl_team_record_500w(league_name,match_time,home_team,visiting_team,score,result,team_id,create_time) values('{}','{}','{}','{}','{}','{}',{},'{}');".format(item['league_name'],item['match_time'],item['home_team'],item['visiting_team'],item['score'],item['result'],item['team_id'],now_time)
            self.cur.execute(sql)
            self.db.commit()
            print("插入{}成功!".format(item['team_id']))
        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
from datetime import datetime

class DlSeasonMatchPipeline(object):
    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):

        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.db.ping(reconnect=True)
            desc = self.cur.execute("select * from dl_season_group_data_500w where match_group_id={} and match_time='{}' and home_team_id={}".format(item['match_group_id'],item['match_time'],item['home_team_id']))
        except:
            desc = self.cur.execute(
                "select * from dl_season_group_data_500w where match_group_id={} and match_time='{}' and home_team_id={}".format(
                    item['match_group_id'], item['match_time'], item['home_team_id']))
        if item['group_name']:
            if desc:
                sql = "update dl_season_group_data_500w set match_score='{}' where match_group_id={} and match_time='{}' and home_team_id={}".format(item['match_score'],item['match_group_id'],item['match_time'],item['home_team_id'])
                ts = "更新{}成功!".format(item['match_group_id'])
            else:
                sql = "insert into dl_season_group_data_500w(match_group_id,match_time,home_team_id,home_team,visitor_team_id,visitor_team,match_score,create_time,group_name) values({},'{}',{},'{}',{},'{}','{}','{}','{}')".format(item['match_group_id'],item['match_time'],item['home_team_id'],item['home_team'],item['visitor_team_id'],item['visitor_team'],item['match_score'],now_time,item['group_name'])
                ts = "插入{}成功!".format(item['match_group_id'])

        else:
            if desc:
                sql = "update dl_season_group_data_500w set match_score='{}' where match_group_id={} and match_time='{}' and home_team_id={}".format(item['match_score'],item['match_group_id'],item['match_time'],item['home_team_id'])
                ts = "更新{}成功!".format(item['match_group_id'])

            else:
                sql = "insert into dl_season_group_data_500w(match_group_id,match_time,home_team_id,home_team,visitor_team_id,visitor_team,match_score,create_time) values({},'{}',{},'{}',{},'{}','{}','{}')".format(item['match_group_id'],item['match_time'],item['home_team_id'],item['home_team'],item['visitor_team_id'],item['visitor_team'],item['match_score'],now_time)
                ts = "插入{}成功!".format(item['match_group_id'])

        self.cur.execute(sql)
        self.db.commit()
        print(ts)
        return item

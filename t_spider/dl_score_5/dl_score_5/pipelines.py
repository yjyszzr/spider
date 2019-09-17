# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
from datetime import datetime

class DlScore5Pipeline(object):

    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()

    def process_item(self, item, spider):
        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')
        desc = self.cur.execute("select * from dl_score_500w where ty='{}' and team_id={} and season_id ={}".format(item['type'],item['team_id'],item['season_id']))
        if desc:
            sql = "update dl_score_500w set ty='{}',team_name='{}',rank={},match_num={},match_h={},match_d={},match_a={},ball_in={},ball_lose={},score={},team_id={} where season_id={} and ty='{}' and team_id={};".format(item['type'],item['team_name'],item['order'],item['match_num'],item['match_h'],item['match_d'],item['match_a'],item['ball_in'],item['ball_lose'],item['score'],item['team_id'],item['season_id'],item['type'],item['team_id'])
            ts = "更新{}成功!".format(item['season_id'])
        else:
            sql = "insert into dl_score_500w(l_id,ty,team_name,match_num,match_h,match_d,match_a,ball_in,ball_lose,score,rank,team_id,season_id,create_time) values({},'{}','{}',{},{},{},{},{},{},{},{},{},{},'{}')".format(item['l_id'],item['type'],item['team_name'],item['match_num'],item['match_h'],item['match_d'],item['match_a'],item['ball_in'],item['ball_lose'],item['score'],item['order'],item['team_id'],item['season_id'],now_time)
            ts = "插入{}成功!".format(item['season_id'])
        self.cur.execute(sql)
        self.db.commit()
        print(ts)
        return item

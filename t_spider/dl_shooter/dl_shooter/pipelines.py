# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
from datetime import datetime


class DlShooterPipeline(object):

    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):
        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')
        desc = self.cur.execute('select * from dl_league_shooter where id={}'.format(item['id']))
        if desc:
            sql = "update dl_league_shooter set sort={},player_name='{}',player_team='{}',in_num={} where id={};".format(item['sort'],item['player_name'],item['team_name'],item['play_num'],item['id'])
            ts = "更新{}成功!".format(item['id'])

        else:
            sql = "insert into dl_league_shooter(match_season_id,player_name,player_team,in_num,league_from,create_time,id) values({},'{}','{}',{},1,'{}',{})".format(item['season_id'],item['player_name'],item['team_name'],item['play_num'],now_time,item['id'])
            ts = "插入{}成功!".format(item['id'])
        self.cur.execute(sql)
        self.db.commit()
        print(ts)
        return item

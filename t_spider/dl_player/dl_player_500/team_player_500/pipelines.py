# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
from datetime import datetime

class TeamPlayer500Pipeline(object):

    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):
        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')

        desc = self.cur.execute('select * from dl_league_player where player_id={} and team_id = {};'.format(item['player_id'],item['team_id']))
        if desc:
            sql = "update dl_league_player set player_name='{}',player_no={},player_type={},birthday='{}',age={},contry='{}',player_price='{}',height='{}',weight='{}' where player_id={} and team_id={};".format(item['player_name'],item['player_num'],item['player_type'],item['birthday'],item['age'],item['contry'],item['player_price'],item['height'],item['weight'],item['player_id'],item['team_id'])
            ts = '更新{}成功!'.format(item['player_id'])
        else:
            sql = "insert into dl_league_player(player_id,player_name,player_no,player_type,team_id,birthday,age,contry,player_price,height,weight,league_from,create_time) values({},'{}',{},{},{},'{}',{},'{}','{}','{}','{}',1,'{}');".format(item['player_id'],item['player_name'],item['player_num'],item['player_type'],item['team_id'],item['birthday'],item['age'],item['contry'],item['player_price'],item['height'],item['weight'],now_time)

            ts = '插入{}成功!'.format(item['player_id'])
        self.cur.execute(sql)
        self.db.commit()
        print(ts)

        return item

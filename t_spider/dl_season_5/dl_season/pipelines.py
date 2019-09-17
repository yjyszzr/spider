# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
from datetime import datetime

class DlSeasonPipeline(object):
    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.close()

    def process_item(self, item, spider):

        try:
            now = datetime.now()
            now_time = now.strftime('%Y-%m-%d %H:%M:%S')
            self.cur.execute('select league_id from dl_league_500w where league_abbr ="{}"'.format(item['league_name']))
            league_id = self.cur.fetchone()[0]
            desc = self.cur.execute('select * from dl_season_500w where season_id={}'.format(item['season_id']))
            if desc:
                print("暂不需要更新")
            else:
                sql = "insert into dl_season_500w(league_id,season_id,match_season,create_time) values({},{},'{}','{}')".format(league_id,item['season_id'],item['season'],now_time)
                self.cur.execute(sql)
                self.db.commit()
                print("插入成功{}".format(league_id))
        except Exception as e:
            print(e)
        return item

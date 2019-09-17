# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
import time
from datetime import datetime

class DlMatchNbaPipeline(object):
    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',
                     charset='utf8')
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):
        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')
        sq1 = "select * from dl_match_basketball where changci_id={};".format(item['changci_id'])
        sq2 = "select * from dl_match_play_basketball where changci_id = {} and play_type={};".format(item['changci_id'], item['play_type'])

        # dl_match判断是插入还是更新的条件
        try:
            cond1 = self.cur.execute(sq1)
            # dl_match_play判断是插入还是更新条件
            if cond1:
                sql = "update dl_match_basketball set home_team_rank='{}',visiting_team_rank='{}' where changci_id={}".format(
                    item['home_team_rank'], item['visiting_team_rank'], item['changci_id'])
                self.cur.execute(sql)
                self.db.commit()
                print("match_nba成功更新>{}".format(item['changci_id']))
            else:

                sql = "insert into dl_match_basketball(league_name,league_abbr,changci_id,changci,home_team_id,home_team_name,home_team_abbr,home_team_rank,visiting_team_id,visiting_team_name,visiting_team_abbr,visiting_team_rank,match_time,show_time,is_show,match_sn,create_time) values('{}','{}',{},'{}',{},'{}','{}','{}',{},'{}','{}','{}','{}','{}',{},'{}','{}');".format(
                    item['league_name'], item['league_abbr'], item['changci_id'], item['changci'], item['home_team_id'],
                    item['home_team_name'], item['home_team_abbr'], item['home_team_rank'], item['visiting_team_id'],
                    item['visiting_team_name'], item['visiting_team_abbr'], item['visiting_team_rank'], item['match_time'],
                    item['show_time'], item['is_show'], item['match_sn'], now_time)
                # print(sql)
                self.cur.execute(sql)
                self.db.commit()
                print("match_nba成功插入%s" % item['changci_id'])
        except Exception as e:
            print(2)

        #篮球玩法
        try:
            print(type(item['play_type']))
            cond2 = self.cur.execute(sq2)
            if cond2:
                sql = 'update dl_match_play_basketball set play_content="{}",update_time="{}" where changci_id={} and play_type={};'.format(item['play_content'], now_time, item['changci_id'], item['play_type'])
                self.cur.execute(sql)
                self.db.commit()
                print("match_play_nba成功更新{}--{}" .format(item['changci_id'], item['play_type']))
            else:
                sql = 'insert into dl_match_play_basketball(changci_id,play_content,play_type,create_time,update_time,status,is_del,is_hot) values({},"{}",{},"{}","{}",{},{},{});'.format(item['changci_id'], item['play_content'], item['play_type'], now_time, now_time, 0, 0,0)
                self.cur.execute(sql)
                self.db.commit()
                print("match_play_nba成功插入{}--{}".format(item['changci_id'],item['play_type']))
        except Exception as f:
            print(f)
        return item

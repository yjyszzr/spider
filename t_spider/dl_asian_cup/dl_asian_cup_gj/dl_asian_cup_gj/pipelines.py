# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect

class DlAsianCupGjPipeline(object):
    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):
        desc = self.cur.execute("select * from dl_asian_cup_gj where rank_id={}".format(item['rank_id']))

        if desc:
            sql = "update"
        else:
            sql = "insert into dl_asian_cup_gj(rank_id,contry_name,prizes,pr,p_id,name,odds_type,jc_id,status,pic) values({},'{}','{}','{}','{}','{}','{}','{}',{},'{}')".format(item['rank_id'],item['contry_name'],item['prizes'],item['pr'],item['p_id'],item['name'],item['odds_type'],item['jc_id'],item['status'],item['pic'])
            self.cur.execute(sql)
            self.db.commit()
            print("插入{}成功!".format(item['contry_name']))
        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect

class DlLeagueRulePipeline(object):

    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):

        sql = "update dl_league_500w set league_rule='{}' where league_abbr = '{}';".format(item['rule'],item['league_addr'])
        try:
            self.cur.execute(sql)
            self.db.commit()
            print("更新>{}<成功!".format(item['league_addr']))
        except Exception as e:
            print('错误信息>{}'.format(e))

        return item

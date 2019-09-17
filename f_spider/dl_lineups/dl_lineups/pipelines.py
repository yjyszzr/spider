# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect

class DlLineupsPipeline(object):
    def __init__(self):
        #测试
        #self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        #正式
        self.db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X',database='cxm_lottery', charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):

        sq = "select * from dl_match_lineups where changci_id={};".format(item['changci_id'])
        desc = self.cur.execute(sq)
        if desc:
            sql = "update dl_match_lineups set match_lineups='{}' where changci_id={};".format(item['data'], item['changci_id'])

            ss = "更新>>%s成功" % item['changci_id']
        else:

            sql = "insert into dl_match_lineups(changci_id,match_lineups) values({},'{}');".format(item['changci_id'], item['data'])

            ss = "插入>>%s成功" % item['changci_id']
        self.cur.execute(sql)
        self.db.commit()
        print(ss)
        return item
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
import datetime

class DlBifenNbaPipeline(object):
    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()
    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):

        if "23:59" in item['match_date']:

            dt = datetime.datetime.strptime('{}'.format(item['match_date']), '%m-%d %H:%M')
            item['match_date'] = (dt + datetime.timedelta(minutes=1)).strftime("%m-%d %M:%S")
        s = "select changci_id from dl_match_basketball where changci = '{}' and match_time like '%{}%';".format(item['changci'],item['match_date'])
        print(s)
        self.cur.execute(s)
        changci_id = self.cur.fetchone()[0]
        desc = self.cur.execute("select * from dl_match_basketball where changci_id = {} and status='0';".format(changci_id))
        if desc and item['whole']:
            sql = "update dl_match_basketball set whole='{}',status='{}' where changci_id={};".format(item['whole'],'1',changci_id)
            # self.cur.execute(sql)
            # self.db.commit()
            print("更新>>{}成功!!".format(changci_id))
        else:
            print('hello')

        return item
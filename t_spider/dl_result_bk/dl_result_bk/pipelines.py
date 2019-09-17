# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
from datetime import datetime

class DlResultBkPipeline(object):

    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.close()

    def process_item(self, item, spider):

        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')
        self.cur.execute("select changci_id from dl_match_basketball where changci = '{}' and match_time like '%{}%'".format(item['match_num'],item['match_time']))
        changci_id = self.cur.fetchone()[0]
        desc = self.cur.execute("select * from dl_result_basketball where changci_id={}".format(changci_id))
        if desc:
            print("暂不更新")
        else:
            try:
                sql = 'insert into dl_result_basketball(changci_id,data_json,create_time) values({},"{}","{}")'.format(changci_id,item,now_time)
                self.cur.execute(sql)
                self.db.commit()
                print("插入{}成功!".format(changci_id))
            except Exception as e:
                print(e)
        return item

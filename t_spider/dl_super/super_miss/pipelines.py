# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import connect
import time
from datetime import datetime

class SuperMissPipeline(object):
    def __init__(self):
        db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        cur = db.cursor()
        self.db = db
        self.cur = cur

    def process_item(self, item, spider):
        now = datetime.now()
        now_time = now.strftime('%Y-%m-%d %H:%M:%S')


        s = "select * from dl_super_lotto_drop where term_num={};".format(item['term_num'])
        desc = self.cur.execute(s)
        if desc:
            sql = "update dl_super_lotto_drop set pre_drop='{}',post_drop='{}' where term_num={};".format(item['pre_drop'],item['post_drop'],item['term_num'])
            ts = "更新成功>{}".format(item['term_num'])
        else:
            sql = "insert into dl_super_lotto_drop(term_num,pre_drop,post_drop,create_time) values({},'{}','{}','{}');".format(item['term_num'],item['pre_drop'],item['post_drop'],now_time)
            ts = "插入成功>{}".format(item['term_num'])
        self.cur.execute(sql)
        self.db.commit()
        print(ts)
        return item

    def __del__(self):
        self.cur.close()
        self.db.close()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pymysql import connect
import time

class JcMatchPipeline(object):
    def __init__(self):
        self.db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.close()

    def process_item(self, item, spider):
        s = "select * from dl_article_info where title='{}' and date='{}';".format(item['title'],item['date'])
        desc = self.cur.execute(s)
        if not desc:
            if item['data']:
                sql = """insert into dl_article_info(date,content,title,source,create_time,status,extend_cat) values('{}',"{}",'{}','{}',{},{},{});""".format(item['date'],item['data'],item['title'],item['ref'],int(time.time()),0,item['extend_cat'])
                self.cur.execute(sql)
                self.db.commit()

        return item

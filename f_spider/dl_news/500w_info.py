import os
import re
import time
import requests
from pymysql import connect
import json

class Info(object):

    def __init__(self):

        self.db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()
        self.url = 'http://zx.500.com/ajax.php?pageCount=0&sortid=1&type=news'
    def __del__(self):
        self.cur.close()
        self.db.close()
    def get_data(self,url=None):
        if url:
            res = requests.get(url=url).content.decode('gbk')
        else:
            res = requests.get(url=self.url).content.decode('gbk')
        return res
    def parse(self,res):
        data = json.loads(res)['data']
        urls = []
        for i in data:
            url = i['url']
            urls.append(url)
        return urls
    def parse_item(self,res):
        item = {}
        item['data'] = re.findall('freeContent">(.*?)</div>', res, re.S)[0]
        item['title'] = re.search('<h1>(.*?)</h1>', res).group(1)
        item['date'] = re.search('icon-time"></i>(.*?)</span>', res, re.S).group(1)
        if '"' in item['data']:
            item['data'] = re.sub('"', "'", item['data'])
        return item
    def save_data(self,item):
        s = "select * from dl_article_info where title='{}' and date='{}';".format(item['title'],item['date'])
        desc = self.cur.execute(s)
        if not desc:
            sql = """insert into dl_article_info(date,content,title,source,create_time,status) values('{}',"{}",'{}','{}',{},{});""".format(item['date'], item['data'], item['title'], '500万', int(time.time()), 0)

            self.cur.execute(sql)
            self.db.commit()
        else:
            print('该标题已存在')

    def run(self):
        res = self.get_data()
        urls = self.parse(res)
        for url in urls:
            res = self.get_data(url)
            item = self.parse_item(res)
            self.save_data(item)

if __name__ == '__main__':
    while True:
        try:
            info = Info()
            info.run()
        except Exception as e:
            print("错误信息为>>%s"%e)
        time.sleep(60)





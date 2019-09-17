# -*- coding: utf-8 -*-
import scrapy
from pymysql import connect
import time
import json
import re
import datetime
from dl_lineups.items import DlLineupsItem


class LineupsSpider(scrapy.Spider):
    name = 'lineups'
    allowed_domains = ['sporttery.cn']
    def start_requests(self):
        s = time.strftime('%Y-%m')
        d = time.strftime('%d')
        # 今天
        today = datetime.date.today()
        day = datetime.timedelta(days=1)
        # 昨天
        pr_day = today - day
        # 昨日
        p_day = str(pr_day)
        # 今日
        t_day = str(today)
        # 明日
        m_day = str(today + day)
        # 后天
        h_day = str(today + day + day)
        # 大后天
        d_day = str(today + day + day + day)
        #正式环境
        db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X',
                     database='cxm_lottery', charset='utf8')
        #测试环境
        # db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',
        #              charset='utf8')
        cur = db.cursor()

        s = "select changci_id from dl_match where match_time like '{}%' or match_time like '{}%' or match_time like '{}%' or match_time like '{}%' or match_time like '{}%';".format(
            pr_day, t_day, m_day, h_day, d_day)
        cur.execute(s)
        ids = cur.fetchall()
        cur.close()
        db.close()
        for id in ids:
            changci_id = id[0]
            url = "http://i.sporttery.cn/api/match_info_live_2/get_match_lineups?m_id={}".format(changci_id)
            yield scrapy.Request(url=url,meta={'changci_id':changci_id})
    def parse(self, response):
        item = DlLineupsItem()
        item['changci_id'] = response.meta['changci_id']
        res = response.body.decode()
        data = json.loads(res)['data']
        if data:
            item['data'] = json.dumps(data, ensure_ascii=False)
            if "'" in item['data']:
                item['data'] = re.sub("'", "`", item['data'])
        else:
            item['data'] = ''
        yield item

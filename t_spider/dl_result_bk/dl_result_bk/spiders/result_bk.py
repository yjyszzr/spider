# -*- coding: utf-8 -*-
import scrapy
import re
from dl_result_bk.items import DlResultBkItem
import datetime
import time
import requests
import re
from datetime import datetime


class ResultBkSpider(scrapy.Spider):
    name = 'result_bk'
    allowed_domains = ['500.com','sporttery.cn']
    start_urls = ['http://zx.500.com/jclq/kaijiang.php']
    # def start_requests(self):
    #     for i in range(16,20):
    #         url = "http://zx.500.com/jclq/kaijiang.php?playid=0&ggid=0&d=2018-09-{}".format(i)
    #         yield scrapy.Request(url=url)
    def parse(self, response):
        data = response.body.decode('gbk')
        datas = re.findall('<td>周.*?</td>.*?</tr>',data,re.S)
        if datas:
            for d in datas:
                item = DlResultBkItem()
                item['match_num'] = re.search('<td>(周.*?)</td>',d).group(1)
                item['match_time'] = re.search('<td.*?class="eng">(\d+-\d+.*?\d+:\d+)</td>',d).group(1)
                item['mnl_score'] = re.search('<td.*?class="eng">(\d+:\d+)</td>',d).group(1)
                item['mnl_result'] = re.search('<td.*?class="eng">\d+:\d+</td>.*?<td.*?>(.*?)</td>',d,re.S).group(1)
                item['hdc_let'] = re.search('<td>周.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?<span.*?>(.*?)</span>.*?</td>',d,re.S).group(1)
                item['hdc_result'] = re.search('<td>周.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>(.*?)</td>',d,re.S).group(1)
                item['wnm_result'] = re.search('<td>周.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>(.*?)</td>',d,re.S).group(1)
                item['hilo_score'] = re.search('<td>周.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>(.*?)</td>',d,re.S).group(1)
                item['hilo_result'] = re.search('<td>周.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>.*?</td>.*?<td.*?>(.*?)</td>',d,re.S).group(1)
                item['league_from'] = 1
                if '23:59' in item['match_time']:
                    dt = datetime.datetime.strptime(item['match_time'], '%m-%d %H:%M')
                    item['match_time'] = (dt + datetime.timedelta(minutes=1)).strftime("%m-%d %M:%S")

                if item['mnl_result'] =='':
                    now = datetime.now()
                    now_time = now.strftime('%Y-%m-%d')
                    url = 'http://info.sporttery.cn/basketball/match_result.php?page=1&lid=0&tid=0&start_date=%s'%now_time
                    res = requests.get(url=url).content.decode('gbk')
                    changci_id = re.search('{}.*?href="http://info.sporttery.cn/basketball/info/bk_match_info.php\?m=(\d+)"'.format(item['match_num']),res,re.S).group(1)
                    yield scrapy.Request(url="http://info.sporttery.cn/basketball/pool_result.php?id={}".format(changci_id),callback=self.parse_it,meta={'data':item})
                else:
                    yield item

        else:
            print("暂无数据")

    def parse_it(self,response):
        data = response.meta['data']
        print(data)

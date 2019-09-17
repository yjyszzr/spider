# -*- coding: utf-8 -*-
import requests
import re
from pymysql import connect
import time
from datetime import datetime

try:

    now = datetime.now()
    now_time = now.strftime('%Y-%m-%d %H:%M:%S')
    #测试机
    db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',
                 charset='utf8')
    cur = db.cursor()


    #大乐透
    url = "http://kaijiang.500.com/dlt.shtml"

    res = requests.get(url=url).content.decode('gbk')
    #大乐透期号
    term_num = re.search('<font class="cfont2"><strong>(.*?)</strong>',res).group(1)
    #大乐透奖池
    prizes = re.search('奖池滚存.*?class="cfont1">(.*?)</span>',res).group(1)
    #开奖日期
    prize_date = re.findall('"span_right">开奖日期.*?(\d+)年(\d+)月(\d+)日.*?兑奖',res)[0]

    y,m,d = prize_date

    if m.startswith('0'):
        pass
    else:
        if int(m) <10:
            m = '0' + m
        if int(d) <10:
            d = '0' + d
    prize_date = y + '-' + m + '-' + d
    # 开奖号码
    num1 = re.findall('"ball_red">(\d+)</li>',res)
    num2 = re.findall('"ball_blue">(\d+)</li>',res)
    prize_num = num1 + num2
    prize_num = ','.join(prize_num)

    s = "select * from dl_super_lotto where term_num={};".format(term_num)
    desc = cur.execute(s)
    if desc:
        sql = "update dl_super_lotto set prize_date='{}',prize_num='{}',prizes='{}' where term_num = {};".format(prize_date,prize_num,prizes,term_num)
        ts = "更新成功>{}".format(term_num)
    else:

        sql = "insert into dl_super_lotto(term_num,prize_date,prize_num,prizes,create_time) values({},'{}','{}','{}','{}');".format(term_num,prize_date,prize_num,prizes,now_time)
        ts = "插入成功>{}".format(term_num)
    cur.execute(sql)
    db.commit()
    print(ts)
except Exception as e:
    print("异常错误为:{}".format(e))
cur.close()
db.close()
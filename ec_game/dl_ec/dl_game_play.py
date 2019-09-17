# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from pymysql import connect
import json
import requests
import re
from datetime import datetime
now = datetime.now()
now_time = now.strftime('%Y-%m-%d %H:%M:%S')


db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()

url = "https://www.365-848.com/SportsBook.API/web?lid=10&zid=0&pd=%23AS%23B151%23&cid=42&ctid=42"
header={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
}

res = requests.get(url=url,headers=header).content.decode()
ls = re.findall('NA=(.*?);.*?PD=(.*?);',res)
for name,id in ls:
    try:
        if name != '电子竞技':

            play_id = re.search('#AC#B151#.*?#D1#(.*?)#F2#',id).group(1)
            game_id = re.search('#AC#B151#(.*?)#D1#.*?#F2#',id).group(1)
            sql = "insert into dl_ec_play(play_id,play_name,game_id,create_time) values('{}','{}','{}','{}')".format(play_id,name,game_id,now_time)
            cur.execute(sql)
            db.commit()
            print('插入{}成功!'.format(name))
    except Exception as e:
        print(e)
cur.close()
db.close()
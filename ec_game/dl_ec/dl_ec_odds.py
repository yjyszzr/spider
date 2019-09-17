# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from pymysql import connect
import json
import requests
import re
import time
from datetime import datetime
from urllib.parse import quote


try :
    now = datetime.now()
    now_time = now.strftime('%Y-%m-%d %H:%M:%S')
    header={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36"
    }


    db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
    cur = db.cursor()
    cur.execute("select game_id from dl_ec_game_name where is_exist =1 ;")
    ids = cur.fetchall()

    for i, in ids:
        try:
            cur.execute("select play_id from dl_ec_play where game_id ='{}';".format(i))
            plays = cur.fetchall()
            for j, in plays:
                try:
                    #中文版
                    pd = '#AC#B151#{}#D1#{}#F2#'.format(i, j)
                    pd = quote(pd)
                    url = "https://www.365-848.com/SportsBook.API/web?lid=10&zid=0&pd={}&cid=42&ctid=42".format(pd)
                    res = requests.get(url=url, headers=header).content.decode()
                    res = re.sub('NA=独赢.*?;','',res)
                    data = re.findall("SY=cw;NA=(.*?);(.*?IT=cw.*?CN=1;)",res)
                    for match_name,k in data:
                        da = re.findall("IT=cw.*?;NA=(.*?);OD=(.*?);",k)
                        for h_name,h_odds in da:
                            try:
                                h_odds = "%.3f"%eval(h_odds)
                                desc = cur.execute("select * from dl_ec_odds where match_name = '{}' and h_name='{}' and play_id='{}';".format(match_name,h_name,j))
                                if desc:
                                    sql = "update dl_ec_odds set h_odds='{}' where match_name='{}' and h_name='{}' and play_id ='{}'".format(h_odds,match_name,h_name,j)
                                    ts = "更新{}成功!".format(h_name)
                                else:
                                    sql = "insert into dl_ec_odds(match_name,h_name,h_odds,play_id,game_id) values('{}','{}','{}','{}','{}')".format(match_name,h_name,h_odds,j,i)
                                    ts = "插入{}成功!".format(h_name)
                                cur.execute(sql)
                                db.commit()
                                print(ts)
                            except:
                                pass
                    time.sleep(3)


                    #英文版
                    pd = '#AC#B151#{}#D1#{}#F2#'.format(i, j)
                    pd = quote(pd)
                    url = "https://www.365-848.com/SportsBook.API/web?lid=1&zid=3&pd={}&cid=42&ctid=42".format(pd)

                    res = requests.get(url=url, headers=header).content.decode()
                    # res = re.sub('NA=独赢.*?;', '', res)

                    data = re.findall("SY=cw;NA=(.*?);(.*?.*?IT=cw.*?)CN=1;", res)

                    for match_name_en,k in data:

                        da = re.findall("IT=cw-.*?;NA=(.*?);OD=(.*?);", k)

                        for h_name_en,ss in da:
                            try:

                                sql = "update dl_ec_odds set match_name_en='{}',h_name_en='{}' where match_name='{}' and h_name='{}' and play_id ='{}'".format(match_name_en,h_name_en,match_name, h_name, j)

                                ts = "更新{}成功!".format(h_name_en)
                                cur.execute(sql)
                                db.commit()
                                print(ts)
                            except:
                                print('错')
                    time.sleep(3)

                except Exception as e:
                    print(e)

        except:
            print('第一层循环错误')
    cur.close()
    db.close()
except:
    print('最外层错误')
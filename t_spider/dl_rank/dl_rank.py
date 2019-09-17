import  requests
import time
import re
from pymysql import connect
import json


while True:
    try:
        db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',
                     charset='utf8')
        cur = db.cursor()
        sql = 'select changci_id from dl_match where DATEDIFF(show_time,NOW()) >= 0 and is_del = 0 and is_show=1 and TIMESTAMPDIFF(MINUTE, match_time, NOW()) < 10'
        cur.execute(sql)
        ids = cur.fetchall()
        for i in ids:
            try:
                id = i[0]
                s = "select home_team_rank,visiting_team_rank from dl_match where changci_id={};".format(id)
                cur.execute(s)
                h_id,a_id = cur.fetchall()[0]
                sq = ''

                url = "http://i.sporttery.cn/api/fb_match_info/get_match_info?mid={}".format(id)
                res = requests.get(url=url).content.decode()
                dict = json.loads(res)["result"]

                if dict['table_h']:
                    sq = "update dl_match set home_team_rank={},visiting_team_rank={} where changci_id={};".format(dict['table_h'], dict['table_a'], id)

                    print("table>>{}".format(sq))
                elif dict['rank_h']:
                    sq = "update dl_match set home_team_rank={},visiting_team_rank={} where changci_id={};".format(dict['rank_h'], dict['rank_a'], id)
                    print("rank_h>>{}".format(sq))
                else:
                    sq = "update dl_match set home_team_rank='{}',visiting_team_rank='{}' where changci_id={};".format('', '',id)

                    print("空>>{}".format(sq))
                cur.execute(sq)
                db.commit()
                time.sleep(1)
            except:
                print('访问错误')
        cur.close()
        db.close()
        print("爬虫执行完毕,休息10分钟...")
        time.sleep(600)
    except Exception as e:
        print(e)



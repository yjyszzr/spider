import requests
from pymysql import connect
import json
import time

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',
             charset='utf8')
cur = db.cursor()
s = "select changci_id from dl_match_nba where league_id = 0;"
cur.execute(s)
ids = cur.fetchall()
for i in ids:
    try:
        changci_id = i[0]
        url = "http://i.sporttery.cn/api/bk_match_info/get_match_info?mid=" + str(changci_id)
        res = requests.get(url=url).content.decode()
        data = json.loads(res)['result']['l_id_dc']
        sql = "update dl_match_nba set league_id={} where changci_id={};".format(data,changci_id)
        cur.execute(sql)
        db.commit()
        print("更新成功%d"%changci_id)
    except Exception as e:
        print('错误信息为>>%s,changci_id为:%d'%(e,changci_id))
    time.sleep(5)
cur.close()
db.close()

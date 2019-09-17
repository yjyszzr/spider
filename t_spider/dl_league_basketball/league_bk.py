import requests
from pymysql import connect
import json
import time

db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',
             charset='utf8')
cur = db.cursor()
s = "select changci_id from dl_match_basketball where league_id = 0 or league_id = -1;"
# s = "select changci_id from dl_match_basketball where league_abbr = '世预男篮';"
cur.execute(s)
ids = cur.fetchall()
for i, in ids:
    try:
        changci_id = i
        url = "http://i.sporttery.cn/api/bk_match_info/get_match_info?mid=" + str(changci_id)
        res = requests.get(url=url).content.decode()
        data = json.loads(res)['result']
        league_id = int(data['l_id_dc'])
        league_abbr = data['l_cn_abbr']
        if league_id == 286:
            league_abbr = '美世预男篮'
        elif league_id == 233:
            league_abbr = '欧世预男篮'
        elif league_id == 287:
            league_abbr = '亚世预男篮'
        sql = "update dl_match_basketball set league_id={},league_abbr='{}' where changci_id={};".format(league_id,league_abbr,changci_id)
        cur.execute(sql)
        db.commit()
        print("更新成功%d"%changci_id)
    except Exception as e:
        print('错误信息为>>%s,changci_id为:%d'%(e,changci_id))
    time.sleep(3)
cur.close()
db.close()

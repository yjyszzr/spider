import requests
from pymysql import connect
import time
import json
import re
import datetime



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
db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
cur = db.cursor()
s = "select changci_id from dl_match where match_time like '{}%' or match_time like '{}%' or match_time like '{}%' or match_time like '{}%' or match_time like '{}%';".format(
    pr_day, t_day, m_day, h_day, d_day)
cur.execute(s)
ids = cur.fetchall()

for id in ids:
    try:
        changci_id = id[0]
        url = "http://i.sporttery.cn/api/match_info_live_2/get_match_lineups?m_id={}".format(changci_id)
        res = requests.get(url=url).content.decode()
        data = json.loads(res)['data']
        if data:

            data = json.dumps(data,ensure_ascii=False)
            if "'" in data:
                data = re.sub("'","`",data)
            sq = "select * from dl_match_lineups where changci_id={};".format(changci_id)
            desc = cur.execute(sq)
            if desc:
                sql = "update dl_match_lineups set match_lineups='{}' where changci_id={};".format(data,changci_id)
                # cur.execute(sql)
                # db.commit()
                print("更新>>%s成功"%changci_id)
            else:

                sql = "insert into dl_match_lineups(changci_id,match_lineups) values({},'{}');".format(changci_id,data)
                # cur.execute(sql)
                # db.commit()
                print("插入>>%s成功"%changci_id)

    except:
        pass
    time.sleep(2)

cur.close()
db.close()

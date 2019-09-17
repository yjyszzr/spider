import requests
import re
from lxml import etree
import time
from pymysql import *



class qiu(object):
    def __init__(self):
        self.db = connect(host='172.17.0.100', port=3306, user='cxm_user_rw', password='YNShTBmL1X1X', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()
        self.url = 'http://info.sporttery.cn/football/history/data_center.php'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            }
    def __del__(self):
        self.cur.close()
        self.db.close()
    def get_data(self,url=None):
        try:
            if url == None:
                res = requests.get(url=self.url,headers=self.headers)
                data = res.content.decode('gbk')
            else:
                res = requests.get(url=url,headers=self.headers)
                data = res.content.decode('gbk')
            return data
        except:
            print("访问错误!")
    #解析出每个球队的详情url
    def parse(self,data):
        urls = re.findall('history_data.php\?mid=\d+',data)
        return urls
    #解析数据
    def parse_item(self,data,url):
        try:
            et = etree.HTML(data)
            node_list = et.xpath('//table[@class="league_data"]//tr')
            league_id = re.search('mid=(\d+)',url).group(1)
            print(league_id)
            for node in node_list:
                item = {}
                tm_id = node.xpath('./td/a[@target="_blank"]/@href')
                if len(tm_id) == 1:
                    #联赛ID
                    item['league_id'] = league_id
                    #总排名
                    item['team_order'] = node.xpath('./td[1]/text()')[0]
                    #球队编号
                    item['team_id'] = re.search('tid=(\d+)',tm_id[0]).group(1)
                    #球队名称
                    item['team_name'] = node.xpath('./td/a[@target="_blank"]/text()')[0]
                    # 总比赛场次数
                    item['l_match_num'] = node.xpath('./td[3]/text()')[0]
                    # 总胜场次数
                    item['l_match_h'] = node.xpath('./td[4]/text()')[0]
                    #总平场次数
                    item['l_match_d'] = node.xpath('./td[5]/text()')[0]
                    #总负场次数
                    item['l_match_a'] = node.xpath('./td[6]/text()')[0]
                    #总进球数
                    item['l_ball_in'] = node.xpath('./td[7]/text()')[0]
                    #总失球数
                    item['l_ball_lose'] = node.xpath('./td[8]/text()')[0]
                    #总净球数
                    item['l_ball_clean'] = node.xpath('./td[9]/text()')[0]
                    #总积分
                    item['l_score'] = node.xpath('./td[22]/text()')[0]
                    #主比赛场次数
                    item['h_match_num'] = node.xpath('./td[10]/text()')[0]
                    #主胜场次数
                    item['h_match_h'] = node.xpath('./td[11]/text()')[0]
                    #主平场次数
                    item['h_match_d'] = node.xpath('./td[12]/text()')[0]
                    #主负场次数
                    item['h_match_a'] = node.xpath('./td[13]/text()')[0]
                    #主进球数
                    item['h_ball_in'] = node.xpath('./td[14]/text()')[0]
                    #主失球数
                    item['h_ball_lose'] = node.xpath('./td[15]/text()')[0]
                    #主积分
                    item['h_score'] = int(item['h_match_h'])*3 + int(item['h_match_d'])
                    #客比赛场次数
                    item['v_match_num'] = node.xpath('./td[16]/text()')[0]
                    #客胜场次数
                    item['v_match_h'] = node.xpath('./td[17]/text()')[0]
                    #客平场次数
                    item['v_match_d'] = node.xpath('./td[18]/text()')[0]
                    #客负场次数
                    item['v_match_a'] = node.xpath('./td[19]/text()')[0]
                    #客进球数
                    item['v_ball_in'] = node.xpath('./td[20]/text()')[0]
                    #客失球数
                    item['v_ball_lose'] = node.xpath('./td[21]/text()')[0]
                    #客积分
                    item['v_score'] = int(item['v_match_h'])*3 + int(item['v_match_d'])
                    self.parse_mysql(item)
        except Exception as e:
            print("parse_item>>%s"%e)
    def parse_mysql(self,item):
        try:
            dec = self.cur.execute('select * from dl_match_team_score where team_id = %s' % item['team_id'])

            if dec:
                sql = 'update dl_match_team_score set team_order={},l_match_num={},l_match_h={},l_match_d={},l_match_a={},l_ball_in={},l_ball_lose={},l_ball_clean={},l_score={},h_match_num={},h_match_h={},h_match_d={},h_match_a={},h_ball_in={},h_ball_lose={},h_score={},v_match_num={},v_match_h={},v_match_d={},v_match_a={},v_ball_in={},v_ball_lose={},v_score={},update_time={} where team_id={} and league_id={};'.format(item['team_order'],item['l_match_num'],item['l_match_h'],item['l_match_d'],item['l_match_a'],item['l_ball_in'],item['l_ball_lose'],item['l_ball_clean'],item['l_score'],item['h_match_num'],item['h_match_h'],item['h_match_d'],item['h_match_a'],item['h_ball_in'],item['h_ball_lose'],item['h_score'],item['v_match_num'],item['v_match_h'],item['v_match_d'],item['v_match_a'],item['v_ball_in'],item['v_ball_lose'],item['v_score'],int(time.time()),item['team_id'],item['league_id'])
                self.cur.execute(sql)
                self.db.commit()
                print('更新>>%s成功'%item['team_id'])
            else:

                sql = 'INSERT INTO dl_match_team_score(league_id,team_order,team_id,team_name,l_match_num,l_match_h,l_match_d,l_match_a,l_ball_in,l_ball_lose,l_ball_clean,l_score,h_match_num,h_match_h,h_match_d,h_match_a,h_ball_in,h_ball_lose,h_score,v_match_num,v_match_h,v_match_d,v_match_a,v_ball_in,v_ball_lose,v_score,update_time) VALUES ({},{},{},"{}",{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{});'.format(item['league_id'],item['team_order'],item['team_id'],item['team_name'],item['l_match_num'],item['l_match_h'],item['l_match_d'],item['l_match_a'],item['l_ball_in'],item['l_ball_lose'],item['l_ball_clean'],item['l_score'],item['h_match_num'],item['h_match_h'],item['h_match_d'],item['h_match_a'],item['h_ball_in'],item['h_ball_lose'],item['h_score'],item['v_match_num'],item['v_match_h'],item['v_match_d'],item['v_match_a'],item['v_ball_in'],item['v_ball_lose'],item['v_score'],int(time.time()))

                self.cur.execute(sql)
                self.db.commit()
                print("插入>>%s成功" % item['team_id'])

        except:
            print('mysql写入错误')


    def start(self):
        try:
            data = self.get_data()
            urls = self.parse(data)
            for url in urls:
                url = 'http://info.sporttery.cn/football/history/'+ url
                time.sleep(1)
                pr_data = self.get_data(url)
                self.parse_item(pr_data,url)
        except:
            print("异常")




q = qiu()
q.start()


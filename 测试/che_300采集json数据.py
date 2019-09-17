__date__ = '2018/9/26 0026 09 11:09'
#coding=utf-8
import csv,requests,json,re,time
class Che(object):
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            'Connection': 'close',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36", }
        self.headers_max = {'Connection': 'close'}

    def ip_zhima(self):
        while True:

            proxyHost = "http-dyn.abuyun.com"
            proxyPort = "9020"

            proxyUser = "HD5Z1OL4130NGGBD"
            proxyPass = "5DAD57EB6EA0440A"
            proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host": proxyHost,
                "port": proxyPort,
                "user": proxyUser,
                "pass": proxyPass,
            }
            self.proxies = {

                "https": proxyMeta,
            }
            url = 'http://httpbin.org/ip'
            try:
                res1 = requests.get(url, headers=self.headers_max, proxies=self.proxies)
                if res1.status_code == 200:
                    print('IP:ONE')
                    break
                else:
                    print('______________________________________________________IP:ERROR%s')
                    time.sleep(3)
                    continue
            except:
                print('ProxyError1:')
                time.sleep(3)
                continue
    def get_data(self):
        headers = {
                                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                                                "authority": "dingjia.che300.com",
                                                'Connection': 'close',
                                                # "referer":"https://www.che300.com/pinggu/v1c1m1134332r2017-1g3?click=homepage&rt=1537235954518",

                                                "accept-encoding":"gzip, deflate, br"
                                                }
        with open("che_three_complete.csv","r",encoding='gbk') as csvfile:
            reader = csv.reader(csvfile)
            B = True
            for i in reader:
                # print
                name = i[1] + i[2] + i[3]
                year = i[4]
                mile = int(i[6])/10000
                c_model_id = i[7]
                series_id = i[8]
                brand_id = i[9]
                print(year, mile, c_model_id, series_id, brand_id)
                url = "https://dingjia.che300.com/app/EvalResult/getPreSaleRate?callback=jQuery18303434035274718359_1537235955204&prov=1&city=1&brand={}&series={}&model={}&regDate={}-6&mile={}&_=1537235955552".format(
                    brand_id, series_id, c_model_id,year,mile)
                n = 1
                while True:
                    n += 1
                    try:
                        response = requests.get(url, headers=headers, proxies=self.proxies,timeout=30)
                        print(response.status_code)
                        if response.status_code == 200:
                            break
                    except Exception as e:
                        if n < 5 :
                            print("####",e)
                            continue
                        else:
                            print("requests###")
                            che.ip_zhima()
                # response = requests.get(url, headers=headers)

                date = response.content.decode()
                response1 = re.match('.*?\((.*?)\)', date)
                response2 = json.loads(response1.group(1))
                try:
                    c_price1 = response2["success"][0]["price"]
                    c_price2 = response2["success"][1]["price"]
                    c_price3 = response2["success"][2]["price"]
                    c_price4 = response2["success"][3]["price"]
                    c_price5 = response2["success"][4]["price"]
                    c_price6 = response2["success"][5]["price"]
                    c_price7 = response2["success"][6]["price"]
                except:
                    print(url)


                with open("che_three_data_yanzheng.csv","ab") as f:
                    if B:
                        str = "c_name, c_model_id, c_year, c_load,c_price1, c_price2, c_price3,c_price4, c_price5, c_price6, c_price7\n".encode()
                        f.write(str)
                        B = False
                with open("che_three_data_yanzheng.csv", "ab") as c:
                    str_data = "{},{},{},{},{},{},{},{},{},{},{}\n".format(name,c_model_id,year,mile,c_price1,c_price2,c_price3,c_price4,c_price5,c_price6,c_price7).encode()
                    c.write(str_data)
                        # time.sleep(1)


    def run(self):
        che.ip_zhima()
        che.get_data()

if __name__ == '__main__':
    che = Che()
    che.run()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
import scrapy
import os
from pymysql import connect

class TeamPicPipeline(object):
    def __init__(self):
        self.db = connect(host='39.106.18.39', port=3306, user='caixiaomi', password='cxmtest', database='cxm_lottery',charset='utf8')
        self.cur = self.db.cursor()

    def __del__(self):
        self.cur.close()
        self.db.close()
    def process_item(self, item, spider):
        if item['image_url']:
            sql = "insert into dl_league_team(team_id,sporttery_teamid,team_name,team_addr,team_type,team_pic) values ({},{},'{}','{}','{}','{}');".format(item['team_id'],item['sporttery_teamid'],item['team_name'],item['team_addr'],item['team_type'],item['team_pic'])
        else:
            sql = "insert into dl_league_team(team_id,sporttery_teamid,team_name,team_addr,team_type) values ({},{},'{}','{}','{}');".format(item['team_id'],item['sporttery_teamid'],item['team_name'],item['team_addr'],item['team_type'])
        self.cur.execute(sql)
        self.db.commit()
        print("正在存储{}的数据".format(item['team_id']))
        return item

# class ImagePipeline(ImagesPipeline):
#     IMAGES_STORE = get_project_settings().get("IMAGES_STORE")
#
#     # 用于发起图片请求，发起的图片请求将由下载器下载图片
#     def get_media_requests(self, item, info):
#         if item['image_url']:
#             return scrapy.Request(url=item['image_url'])
#
#     def item_completed(self, results, item, info):
#         # print('----',results)
#         # 获取图片信息
#         images = [data['path'] for ok, data in results if ok]
#         # print(images)
#
#         # 拼接旧文件名
#         old_name = self.IMAGES_STORE + os.sep + images[0]
#         # 拼接新文件名
#         new_name = self.IMAGES_STORE + os.sep + images[0].split(os.sep)[0] + os.sep + item['team_id'] + '.jpg'
#
#         # 重命名
#         os.rename(old_name, new_name)
#
#         return item


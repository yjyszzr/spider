# -*- coding: utf-8 -*-
import os
import time


new_time = time.strftime("%Y-%m-%d")
os.system("""cd /a/logs &&rm -f `ls *.log|egrep -v '({})'`""".format(new_time))
os.system('cat /dev/null > /a/spider/f_spider/dl_asia/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_bifen/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_clear/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_europe/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_future/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_league/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_lineups/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_live/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_match/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_news/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_rank/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_result/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_score/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_sizeBall/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_support/nohup.out')
os.system('cat /dev/null > /a/spider/f_spider/dl_team/nohup.out')
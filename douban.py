# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup
import pymysql
import doubanMisc
import time

db = pymysql.connect(host='localhost', port=3306, user='spider', passwd='spider', db='spider', charset='UTF8')
cursor = db.cursor()

indexUrl = 'https://movie.douban.com'
r = requests.get(indexUrl)
#bid = dict(bid=r.cookies['bid'])
#bid = {'cookie':'bid=zg4DHXGTHKg; ll="118282"; __yadk_uid=rOrcIioLrESrf5UdFEO4qhvxBCrIY1F3; gr_user_id=b565c870-047e-4530-aa71-a3eb53a8687d; viewed="5338398_2567698_26419771"; _vwo_uuid_v2=530619501E034B1BAD160F213E0FE11D|345353f13a9d932ec5918030e84e29fc; ps=y; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1508219095%2C%22https%3A%2F%2Faccounts.douban.com%2Flogin%3Fsource%3Dmovie%22%5D; __utma=30149280.512443565.1489375624.1508214872.1508219151.18; __utmb=30149280.0.10.1508219151; __utmc=30149280; __utmz=30149280.1508219151.18.8.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmv=30149280.16826; __utma=223695111.1120922378.1491191341.1508214872.1508219151.11; __utmb=223695111.0.10.1508219151; __utmc=223695111; __utmz=223695111.1508219151.11.5.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; push_noty_num=0; push_doumail_num=0; ap=1; _pk_id.100001.4cf6=3edc0b5bbc340a50.1491191341.11.1508219172.1508214872.; _pk_ses.100001.4cf6=*; ue="sz547073165@qq.com"; dbcl2="168261917:DIZ1OND56xU"'}
bid = {'Cookie':'bid=zg4DHXGTHKg; ll="118282"; __yadk_uid=rOrcIioLrESrf5UdFEO4qhvxBCrIY1F3; gr_user_id=b565c870-047e-4530-aa71-a3eb53a8687d; viewed="5338398_2567698_26419771"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1511614770%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; ap=1; ps=y; ue="sz547073165@qq.com"; dbcl2="168261917:+MgV8DAHRwA"; ck=ZMLs; _pk_id.100001.4cf6=3edc0b5bbc340a50.1491191341.20.1511615033.1509171888.; _pk_ses.100001.4cf6=*; __utma=30149280.512443565.1489375624.1511168867.1511614768.30; __utmb=30149280.1.10.1511614768; __utmc=30149280; __utmz=30149280.1508557584.23.10.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.16826; __utma=223695111.1120922378.1491191341.1509171868.1511614770.20; __utmb=223695111.0.10.1511614770; __utmc=223695111; __utmz=223695111.1511614770.20.9.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=530619501E034B1BAD160F213E0FE11D|345353f13a9d932ec5918030e84e29fc'}
userAgent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
#print(bid)

movieId = '26322999'#银翼杀手
url = indexUrl+'/subject/'+movieId+'/comments'
nextUrlParam='?start=120&limit=20&sort=new_score&status=P&percent_type='#'?status=P'
isNext=True
while isNext:
    commentsList, nextUrlParam = doubanMisc.getCommentsListAndNextUrl((url+nextUrlParam),bid,userAgent)
    print(nextUrlParam)
    
    if nextUrlParam == '':
        isNext = False
    for comment in commentsList :
        commentObject = doubanMisc.commentsHandler(comment)
        if commentObject != None:
            doubanMisc.saveComment(db,cursor,movieId,commentObject[0],commentObject[1],commentObject[2],commentObject[3],
                                   commentObject[4],commentObject[5])
    time.sleep(1.5) # 休眠1秒
db.close()
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 16:39:19 2017

@author: Administrator
"""
import requests
from bs4 import BeautifulSoup
import re

def getCommentsListAndNextUrl(url,bid,userAgent):
    r = requests.get(url,cookies=bid)
    soup = BeautifulSoup(r.text, "lxml")
    commentsList = soup.find_all(attrs={"class": "comment-item"})
    nextUrlParam=''
    paginator=soup.find(id='paginator').find_all('a')
    if len(paginator)==1 :
        nextUrlParam = soup.find(attrs={"class": "next"})['href']
    elif len(paginator)==3 :
        nextUrlParam = soup.find(attrs={"class": "next"})['href']
    return commentsList,nextUrlParam

def commentsHandler(comments):
    soup = comments
    if soup.text.strip() == '还没有人写过短评':
        return
    votes = soup.find_all(attrs={'class':'votes'})[0].text
    #print('votes='+votes)
    commentInfo = soup.find_all(attrs={'class':'comment-info'})
    userName = commentInfo[0].find('a').text.replace("'","\\\'")
    #print('userName='+userName)
    commentInfoSpanList = commentInfo[0].find_all('span')
    status=''
    star='0'
    time=''
    if len(commentInfoSpanList)==3:
        #看过
        status='P'
        #print('status='+status)
        starStr=commentInfoSpanList[1]['class'][0]
        if starStr=='allstar10':
            star='10'
        elif starStr=='allstar20':
            star='20'
        elif starStr=='allstar30':
            star='30'
        elif starStr=='allstar40':
            star='40'
        else :
            star='50'
        #print('star='+star)
        time=commentInfoSpanList[2]['title']
        #print('time='+time)
    else:
        #想看
        status='F'
        #print('status='+status)
        #print('star='+star)
        if len(commentInfoSpanList) == 1:
            time=commentInfoSpanList[0]['title']
        else:
            time=commentInfoSpanList[1]['title']
        #print('time='+time)
    comment=soup.find_all('p')[0].text.replace("'","\\\'")
    #print('comment='+comment)
    return userName, status, star, time, comment, votes

def saveComment(db,cursor,movieId,userName,status,star,time,comment,votes):
    selectSql = u'select comment_id from comments where movie_id = '+movieId+' and user_name = \''+userName+'\''
    try:
       # 执行SQL语句
       cursor.execute(remove_emoji(selectSql))
       # 获取所有记录列表
       commentId = cursor.fetchone()
       if commentId != None:
           return
    except:
       print ("select commentes failed")
       print(selectSql)
    sql = u'INSERT INTO comments (movie_id, user_name, status, star, time, comment, votes) VALUES '
    sql += '('+movieId+', \''+userName+'\', \''+status+'\', '+star+', \''+time+'\', \''+comment+'\', '+votes+')'
    #print(sql)
    try:
        # 执行sql语句
        cursor.execute(remove_emoji(sql))
        # 提交到数据库执行
        db.commit()
        print('save commentes success')
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('save commentes failed')
        print(sql)

def remove_emoji(text):
    emoji_pattern = re.compile(u'[\U00010000-\U0010ffff]')
    return emoji_pattern.sub(r'', text)
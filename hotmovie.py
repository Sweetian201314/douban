#!/usr/bin/env python3
#-*-coding:utf-8-*- #编码声明，不要忘记！
import requests
import json
#配置数据库
import pymysql
db = pymysql.connect("localhost","root","Tian19930308","python_learning",charset="utf8")
cursor = db.cursor() #创建游标对象

tag_name=requests.get('https://movie.douban.com/j/search_tags?type=movie')#找到不同分类对应的API，差异在于tag不同
tag_name=json.loads(tag_name.text)['tags']#请求tag,也可以这样写tag_name=tag_name.json()['tags']
movie_url='https://movie.douban.com/j/search_subjects'

movie_list = []
page_limit = 20

for name in tag_name:
    page = 0
    length = 44 #length初始值可以为任意大于0的值，目的是运行循环语句

    while length > 0:
        params = {
            'type': 'movie',
            'sort': 'time',
            'page_limit': page_limit,
            'tag': name,
            'page_start': page
        }

        movie_info = requests.get(movie_url, params=params)#配置参数.
        movie_info = json.loads(movie_info.text)['subjects']
        movie_list = movie_list + movie_info
        page = page + page_limit
        length = len(movie_info)

        for movie in movie_info:

            data = [(movie['title'], movie['rate'], movie['url'], name)]
            print(data)
            cursor.executemany("insert into recent_hot_movie(name,rate,url,kind) values(%s,%s,%s,%s)",data) #执行SQL语句

db.commit()
print('success connect')
print(len(movie_list))






#!/usr/bin/env python
# coding: utf-8

"""
 Created by 仙书 on 2020/1/24
"""

import requests
import re
import json
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

import time
from models import Article
from crawler.db import session

def get_wy_html():
    """
    获取页面html
    :return:
    """
    dx_url = "https://news.163.com/special/00018IRU/virus_report_data.js?_=1579844766151&callback=callback#"
    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection': 'Keep-Alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    res = requests.get(dx_url, headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    
    # htmlfile = open("html.txt","w+")
    # # htmlfile.write(html)
    return html

def get_articles(html):
    html = html.replace(' ','').replace('\t','').replace('\n','')\
        .replace('callback(','').replace(')','').replace(',}',"}")\
        .replace('list','"list"').replace('hospital','"hospital"')
    data = json.loads(html)
    return data


def save_articles(data):
    articles = session.query(Article).all()
    map_data = []
    for article in articles:
        map_data.append(article.title)
    for i in data:
        if i['title'] not in map_data:
            article = Article()
            article_time = i['time']
            article.time = time.strptime(article_time, "%Y.%m.%d%H:%M:%S")
            article.detail = i['detail']
            article.link = i['link']
            article.title = i['title']
            session.add(article)
    session.commit()

def main_jop():
    html = get_wy_html()
    data = get_articles(html)
    save_articles(data['list'])
    
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(main_jop, 'interval', minutes=3, max_instances=1, )
    scheduler.start()


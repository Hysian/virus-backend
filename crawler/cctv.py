#!/usr/bin/env python
# coding: utf-8

"""
 Created by 仙书 on 2020/1/25
"""

import uuid
import requests
import time
import json
from models import CCTVVideo
from crawler.db import session
from sqlalchemy import desc
from apscheduler.schedulers.blocking import BlockingScheduler

def get_page_html():
    """
    获取页面html
    :return:
    """
    dx_url = "http://media.app.cctv.com/vapi/video/vplist.do?chid=EPGC1525679284945000&title=%E7%96%AB%E6%83%85&p=1&n=12&cb=t"
    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection': 'Keep-Alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    res = requests.get(dx_url, headers=headers)
    res.encoding = 'utf-8'
    html = res.text
    return html

def get_result(html):
    html = html.replace('t(','').replace(')','')
    return json.loads(html)

def save_data(data):
    videos = session.query(CCTVVideo).order_by(desc(CCTVVideo.date)).limit(5)
    video_map = []
    for item in videos:
        video_map.append(item.source_url)
    for i in data:
        if i['wwwUrl'] in video_map:
            continue
        video = CCTVVideo()
        video.title = i['title']
        video.source_url = i['wwwUrl']
        video.id = str(uuid.uuid4().hex)
        timeNum = i['pubTime']
        timeStamp = float(timeNum / 1000)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        video.date = otherStyleTime
        session.add(video)
    session.commit()
    
def main_jop():
    html = get_page_html()
    res = get_result(html)
    data = res["data"][:5]
    save_data(data)

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(main_jop, 'interval', minutes=30, max_instances=1, )
    scheduler.start()


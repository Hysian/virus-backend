#!/usr/bin/env python
# coding: utf-8

"""
 Created by 仙书 on 2020/1/25
"""

import re
import time
from models import Count, HubeiCount, ChinaCount, BeiJingCount
from datetime import datetime
from crawler.db import session
from apscheduler.schedulers.blocking import BlockingScheduler


def sync_area_data():
    hubei_count = session.query(Count).filter(Count.area_name == '湖北').first()
    beijing_count = session.query(Count).filter(Count.area_name == '北京').first()
    china_count = session.query(Count).filter(Count.area_name == '全国').first()
    
    hubei = session.query(HubeiCount).first()
    beijing = session.query(BeiJingCount).first()
    china = session.query(ChinaCount).first()
    
    sync_data(hubei, hubei_count)
    sync_data(beijing, beijing_count)
    sync_data(china, china_count)
    session.commit()
    
def sync_data(old, new):
    old.new_case = new.new_case
    old.confirm_case = new.confirm_case
    old.cure_case = new.cure_case
    old.probable_case = new.probable_case
    old.dead_case = new.dead_case


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(sync_area_data, 'interval', minutes=1, max_instances=1, )
    scheduler.start()


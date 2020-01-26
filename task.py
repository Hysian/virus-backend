#!/usr/bin/env python
# coding: utf-8

"""
 Created by 仙书 on 2020/1/23
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from crawler.dxy import get_area_data, get_page_html, get_brief_info
from crawler.dxy_work import  update_province_area_state, update_city_area_state,\
    format_data, save_country_data, save_record_data

# 定时任务
def area_update_job():
    """
    爬取全国、各省市疫情数据入库
    :return:
    """
    html = get_page_html()
    brief_info = get_brief_info(html)
    res = format_data(brief_info)
    save_country_data(res)
    area_state = get_area_data(html)
    update_province_area_state(area_state)
    update_city_area_state(area_state)
   
def area_count_record_job():
    """
    记录各地疫情数据入库
    :return:
    """
    save_record_data()
    


# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(area_update_job, 'interval', minutes=1, max_instances=1,)
scheduler.add_job(area_count_record_job, 'interval', minutes=60, max_instances=1,)
scheduler.start()
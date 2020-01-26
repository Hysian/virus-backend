#!/usr/bin/env python
# coding: utf-8

"""
 Created by 仙书 on 2020/1/24
"""

import re
import time
from models import Count, CountRecord, Article
from datetime import datetime
from crawler.db import session

def json_to_model(model, json):
    model.dead_case = json['deadCount']
    model.cure_case = json['curedCount']
    model.probable_case = json['suspectedCount']
    confirmed = json['confirmedCount']
    if model.confirm_case and confirmed and model.confirm_case != confirmed:
        model.new_case = confirmed - model.confirm_case
    model.confirm_case = confirmed
    if hasattr(json, 'comment'):
        model.memo = json['comment']

def update_city_area_state(res):
    data = session.query(Count).filter(Count.area_type == 'city').all()
    map_data = {}
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for count in data:
        map_data["city_"+count.province+"_"+count.area_name] = count
    for province in res:
        cities = province['cities']
        province = province['provinceShortName']
        for city in cities:
            city_key = city['cityName']
            city_count = map_data.get("city_"+province+"_"+city_key)
            if not city_count:
                city_count = Count()
                city_count.from_source = 'dxy'
                city_count.area_name = city_key
                city_count.area_type = 'city'
                city_count.province = province
                session.add(city_count)
            json_to_model(city_count, city)
            city_count.update_time = now
    session.commit()



def update_province_area_state(res):
    """
    更新各省级数据
    :return:
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = session.query(Count).filter(Count.area_type=='province').all()
    map_data = {}
    for count in data:
        map_data[count.area_name] = count
    for o in res:
        comment = o['comment']
        key = o['provinceShortName']
        count = map_data.get(key)
        if not count:
            count = Count()
            count.from_source = 'dxy'
            count.area_name = key
            count.area_type = 'province'
            count.province = key
            session.add(count)
        json_to_model(count, o)
        if comment != '':
            num_data = format_data(comment)
            filter_data(num_data, count)
        count.update_time = now
    session.commit()

def save_country_data(res):
    """
    保存全国的数据
    :return:
    """
    count = session.query(Count).filter(Count.area_name == '全国').first()
    if not count:
        count = Count()
        count.area_type = 'country'
        count.area_name = '全国'
        count.from_source = 'dxy'
        session.add(count)
    filter_data(res, count)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count.update_time = now
    session.commit()

def save_record_data():
    """
    保存对应记录
    :return:
    """
    counts = session.query(Count).all()
    for count in counts:
        count_record = CountRecord()
        count_record.new_case = count.new_case
        count_record.confirm_case = count.confirm_case
        count_record.cure_case = count.cure_case
        count_record.probable_case = count.probable_case
        count_record.dead_case = count.dead_case
        
        count_record.province = count.province
        count_record.area_type = count.area_type
        count_record.area_name = count.area_name
        count_record.update_time = count.update_time
        count_record.from_source = count.from_source
        
        count_record.memo = count.memo
        session.add(count_record)
    session.commit()

def format_data(brief):
    """
    格式化人数
    :param brief:
    :return:
    """
    rule = [r'确诊(.*?)例',
            r'疑似(.*?)例',
            r'治愈(.*?)例',
            r'死亡(.*?)例']
    data = []
    for item in rule:
        filter1 = re.compile(item)
        brief = str(brief).replace('疑似数据待确认', '')
        result = re.findall(filter1, brief)
        if len(result) != 0:
            num = str(result[0]).strip()
            data.append(num)
        else:
            data.append(0)
    return data

def filter_data(data, model):
    if data[0] != 0:
        model.confirm_case = data[0]
    if data[1] != 0:
        model.probable_case = data[1]
    if data[2] != 0:
        model.cure_case = data[2]
    if data[3] != 0:
        model.dead_case = data[3]

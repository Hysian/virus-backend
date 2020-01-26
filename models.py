#!/usr/bin/env python
# coding: utf-8

"""
 Created by 仙书 on 2020/1/23
"""
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL

from app import db

class Count(db.Model):
    
    __tablename__ = 'china_count_statistics'

    id = Column(Integer, autoincrement=True, primary_key=True, comment='主键')

    from_source = Column(String(50), comment='数据来源')
    confirm_case = Column(Integer, comment='确诊人数')
    probable_case = Column(Integer, comment='疑似人数')
    dead_case = Column(Integer, comment='死亡人数')
    cure_case = Column(Integer, comment='治愈病历')
    new_case = Column(Integer, comment='新增病历')
    update_time = Column(DateTime, comment='更新时间')
    memo =  Column(String(200), comment='附加信息')
    area_name = Column(String(50), comment='地区')
    province = Column(String(50), comment='所属省')
    area_type = Column(String(50), comment='地区等级')

class CountRecord(db.Model):
    
    __tablename__ = 'china_count_statistics_history'
    id = Column(Integer, autoincrement=True, primary_key=True, comment='主键')
    update_time = Column(DateTime, comment='更新时间')
    from_source = Column(String(50), comment='数据来源')
    confirm_case = Column(Integer, comment='确诊人数')
    probable_case = Column(Integer, comment='疑似人数')
    dead_case = Column(Integer, comment='死亡人数')
    cure_case = Column(Integer, comment='治愈病历')
    
    new_case = Column(Integer, comment='新增病历')
    memo =  Column(String(200), comment='附加信息')
    province = Column(String(50), comment='所属省')
    area_name = Column(String(50), comment='地区')
    area_type = Column(String(50), comment='地区等级')

class ChinaCount(db.Model):
    __tablename__ = 'china_statistics'
    id = Column(Integer, autoincrement=True, primary_key=True, comment='主键')
    update_time = Column(DateTime, comment='更新时间')
    confirm_case = Column(Integer, comment='确诊人数')
    probable_case = Column(Integer, comment='疑似人数')
    dead_case = Column(Integer, comment='死亡人数')
    cure_case = Column(Integer, comment='治愈病历')
    new_case = Column(Integer, comment='新增病历')
    memo = Column(String(200), comment='附加信息')

class BeiJingCount(db.Model):
    __tablename__ = 'china_beijing_count_statistics'
    id = Column(Integer, autoincrement=True, primary_key=True, comment='主键')
    update_time = Column(DateTime, comment='更新时间')
    confirm_case = Column(Integer, comment='确诊人数')
    probable_case = Column(Integer, comment='疑似人数')
    dead_case = Column(Integer, comment='死亡人数')
    cure_case = Column(Integer, comment='治愈病历')
    new_case = Column(Integer, comment='新增病历')
    memo = Column(String(200), comment='附加信息')

class HubeiCount(db.Model):
    __tablename__ = 'china_hubei_count_statistics'
    id = Column(Integer, autoincrement=True, primary_key=True, comment='主键')
    update_time = Column(DateTime, comment='更新时间')
    confirm_case = Column(Integer, comment='确诊人数')
    probable_case = Column(Integer, comment='疑似人数')
    dead_case = Column(Integer, comment='死亡人数')
    cure_case = Column(Integer, comment='治愈病历')
    new_case = Column(Integer, comment='新增病历')
    memo = Column(String(200), comment='附加信息')

class Article(db.Model):
    __tablename__ = 'china_real_broadcast'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    link = Column(String(500), comment='链接')
    detail = Column(String(500), comment='内容')
    title = Column(String(500), comment='标题')
    time = Column(DateTime, comment="时间")
    memo = Column(String(500), comment='备注')
   
class Migration(db.Model):
    __tablename__ = 'china_migration_info'
    
    id = Column(String(50), primary_key=True)
    area_id = Column(String(50))
    create_date = Column(String(50), comment='日期')
    migrate_type = Column(String(50), comment='迁移类型')
    
    area_type = Column(String(50), comment='地区类型')
    area_name = Column(String(50), comment='地名')
    
    province_name = Column(String(20), comment='省')
    city_name = Column(String(20),  comment='城市')
    value = Column(DECIMAL(11,2), comment='比例')


class CCTVVideo(db.Model):
    __tablename__ = 'china_real_video_public'
    
    id = Column(String(50), primary_key=True)
    date = Column(DateTime, comment='日期')
    title = Column(String(50), comment='标题')
    source_url = Column(String(500), comment='源url')
    
    is_public = Column(Integer, comment='是否发布', default=0)
    memo = Column(String(50), comment='来源')

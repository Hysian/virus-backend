#!/usr/bin/env python
# coding: utf-8

"""
 Created by Hysian on 2018/9/13
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class Config:
    username=''
    password=''
    ip=''
    database= 'virus'
    port=3306
    
db_config = Config

uri = f'mysql+pymysql://{db_config.username}:{db_config.password}@{db_config.ip}:{db_config.port}/{db_config.database}?charset=UTF8MB4'
engine = create_engine(uri,
                    pool_size=5,  # 连接池大小
                    pool_timeout=30,
                    pool_recycle=-1
                      )


SessionFactory = sessionmaker(bind=engine)
session = scoped_session(SessionFactory)



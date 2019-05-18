#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Leon xie

import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String

engine = create_engine("mysql+mysqlconnector://root:wen123@localhost:3306/nationality",encoding='utf-8',echo=True)
#echo=True，就是把整个过程打印出来
Base=declarative_base() #生成ORM基类

class Nation(Base):
    __tablename__ = 'nation' #表名
    id = Column(Integer,primary_key=True) #字段，整形，主键 column是导入的
    name = Column(String(32))
    population = Column(Integer)
    percent = Column(String(32))

class Distributed(Base):
    __tablename__ = 'distributed' #表名
    id = Column(Integer, primary_key=True)  # 字段，整形，主键 column是导入的
    province = Column(String(32)) #字段，整形，主键 column是导入的
    city = Column(String(32))
    longitude = Column(String(32))
    latitude = Column(String(32))
    nationId = Column(String(32))
    population = Column(Integer)

Base.metadata.create_all(engine) #创建表结构
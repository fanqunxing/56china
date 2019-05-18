import requests
from bs4 import BeautifulSoup  # bs4模块用来解析爬取下来的网页数据
from bs4 import Tag
import jieba
from sqlalchemy import Column,create_engine
from sqlalchemy.types import *
from sqlalchemy.orm import sessionmaker
from Models import Nation
import re


class Spider():
    def getPopulation(self):
        engine = create_engine("mysql+mysqlconnector://root:wen123@localhost:3306/nationality", encoding='utf-8',
                               echo=True)
        # 创建连接数据库引擎
        DBsession = sessionmaker(bind=engine)
        session = DBsession()
        url ="http://114.xixik.com/minority/"
        res=requests.get(url).content.decode("gbk")
        resSoup=BeautifulSoup(res)
        div = resSoup.find_all(name='div', attrs={"class": "lindBox"})[7]
        for content in div.contents:
            if(isinstance(content,Tag)):
                match=re.match(r'[\s\S]*占比[\s\S]*', content.text)
                match2 = re.match(r'[\s\S]*族[\s\S]*', content.text)
                if(match and match2):
                    clean = content.text.replace("\r", "").replace("\n", "").replace(" ", "").replace("\t", "") \
                        .replace("\xa0", "").replace("占比", "").replace("人", "")
                    words = jieba.cut(clean)
                    data = []
                    for word in words:
                        if (len(word) > 1):
                            data.append(word)
                    if(len(data)==3):
                        nation = Nation()
                        nation.name = data[0]
                        nation.population = data[1]
                        nation.percent = data[2]
                        session.add(nation)
                        session.commit()










if __name__ == '__main__':
    Spider().getPopulation()



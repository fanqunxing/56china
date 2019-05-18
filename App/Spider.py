import requests
from bs4 import BeautifulSoup  # bs4模块用来解析爬取下来的网页数据
from bs4 import Tag
import jieba
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from App.Models import Nation
import re
from App.ext import db
import uuid
import time
import os


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



    def getNationDetail(self):
        #engine = create_engine("mysql+mysqlconnector://root:wen123@localhost:3306/nationality", encoding='utf-8',
                              # echo=True)
        # 创建连接数据库引擎
        #DBsession = sessionmaker(bind=engine)
        #session = DBsession()
        nations = Nation.query.filter().all()
        url ="https://jingyan.baidu.com/article/4f7d5712b1c07c1a20192736.html"
        res=requests.get(url).content.decode("utf-8")
        resSoup=BeautifulSoup(res)
        div = resSoup.find_all(name='div', attrs={"class": "exp-content-body"})
        contents=div[1].contents[0].contents
        for content in contents:
            detail=content.contents[1].text
            for nation in nations:
                if(detail.count(nation.name)>0):
                    nation.desc = detail
                    print(detail)
                    img = content.contents[2].contents[0].contents[0].contents[0]
                    url = img.attrs["data-src"]
                    response = requests.get(url)
                    img = response.content
                    fileId=uuid.uuid1().__str__()
                    print(url)
                    print(fileId)
                    nation.fileId=fileId
                    time.sleep(5)

                    with open(upload_path, 'wb') as f:
                        f.write(img)
                        f.close()
                    db.session.add(nation)
                    db.session.commit()

            #imgSoup=BeautifulSoup(img)
            #imgTag=imgSoup.find_all("img")
            #textSoup=BeautifulSoup(content.text)
            #detail=textSoup.find_all(name='div', attrs={"class": "content-list-text"})
            #img=textSoup.find_all(name='img ')

    def download(self):
        url="https://imgsa.baidu.com/exp/w=500/sign=41b8dbb8cd1b9d168ac79a61c3dfb4eb/fc1f4134970a304e1261e99dd2c8a786c9175c11.jpg"
        response = requests.get(url)
        img = response.content
        fileId = uuid.uuid1().__str__()
        with open('data/pic/' + fileId + '.jpg', 'wb') as f:
            f.write(img)
            f.close()







if __name__ == '__main__':
    Spider().download()



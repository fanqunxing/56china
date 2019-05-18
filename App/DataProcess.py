import csv
import jieba
import json
from Models import Nation,Distributed
from sqlalchemy import Column,create_engine
from sqlalchemy.types import *
from sqlalchemy.orm import sessionmaker

class DataProcess():
    def clean(self):
        CityGPSs=self.getCityGPSs()
        f=open("data/distribute_collectt.csv","rt", encoding="utf-8")
        lines=f.readlines()
        for line in lines:
            words=jieba.cut(line)
            rows = []
            for word in words:
                if(len(word)>1):
                    rows.append(word)
            out = open('data/distribute_clean.csv', 'a', newline='', encoding="utf-8")
            csv_writer = csv.writer(out)
            csv_writer.writerow(rows)
        f.close()

    def save2Db(self):
        engine = create_engine("mysql+mysqlconnector://root:wen123@localhost:3306/nationality", encoding='utf-8',
                               echo=True)
        # 创建连接数据库引擎
        DBsession = sessionmaker(bind=engine)
        session = DBsession()


        out = open('data/distribute_clean1.csv', 'r', encoding="utf-8")
        csv_reader=csv.reader(out)
        citys=self.getCityGPSs()
        for row in csv_reader:
            for one in row:
                for city in citys:
                    if(city["city"]==one or city["city"].count("one")>0):
                        distributed=Distributed()
                        distributed.city=city["city"]
                        distributed.longitude =city["longitude"]
                        distributed.latitude = city["latitude"]
                        distributed.nationId = row[0]
                        distributed.province = city["province"]
                        session.add(distributed)
            nation = Nation()
            nation.name = row[0]
            nation.population=row[1]
            session.add(nation)
        session.commit()



    def isProvinceOrCityName(self,name):
        print()



    def getCityGPSs(self):
        f=open("data/gps.txt","rt", encoding="utf-8")
        lines=f.readlines()
        citys=[]
        for line in lines:
            city={}
            words=line.split(",")
            #words=jieba.cut(line)
            data=[]
            wordList=list(words)
            for word in wordList:
                if(len(word)>1):
                    data.append(word.replace("\n",""))
            city["province"] = data[0]
            city["city"] = data[1]
            city["longitude"] = data[2]
            city["latitude"] = data[3]
            citys.append(city)
        #print(citys)
        return citys

    def getProvince(self):
        f = open("data/city_code.json", "rt", encoding="utf-8")
        text=f.read()
        data=json.loads(text)
        print(data)


if __name__ == '__main__':
    DataProcess().save2Db()
    #coupon = Nation.query.filter(Coupon.couponId == couponId).first()
#engine = create_engine("mysql+mysqlconnector://root:wen123@localhost:3306/nationality", encoding='utf-8', echo=True)
    # 创建连接数据库引擎
    #DBsession = sessionmaker(bind=engine)
    #session=DBsession()
    #nation = Nation()
    #nation.name = "123"
    #session.add(nation)
    #session.commit()
import csv
import jieba
import json
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
        out = open('data/distribute_clean1.csv', 'r', encoding="utf-8")
        csv_reader=csv.reader(out)
        citys=self.getCityGPSs()
        for row in csv_reader:
            for one in row:
                for city in citys:
                    if(city["city"]==one or city["city"].count("one")>0):
                        print(one)



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
import requests
from bs4 import BeautifulSoup  # bs4模块用来解析爬取下来的网页数据
from bs4 import Tag
import jieba



class Spider():
    def getPopulation(self):
        url ="http://114.xixik.com/minority/"
        res=requests.get(url).content.decode("gbk")
        resSoup=BeautifulSoup(res)
        div = resSoup.find_all(name='div', attrs={"class": "lindBox"})[7]
        for content in div.contents:
            if(isinstance(content,Tag)):
                clean=content.text.replace("\r","").replace("\n","").replace(" ","").replace("\t","")\
                    .replace("\xa0","").replace("占比","").replace("人","").replace(";","")
                words=jieba.cut(clean)
                

if __name__ == '__main__':
    Spider().getPopulation()



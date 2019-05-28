from flask import make_response,send_from_directory
from App.common.ResData import ResData
from flask import Blueprint, request, jsonify, make_response, session
from App.Models import Nation,Distributed
from App.ext import db
from App.Spider import Spider
import time
import requests
from bs4 import BeautifulSoup
import uuid
import os

nationBlue = Blueprint("nation", __name__)

def init_nationBlue(app):
    app.register_blueprint(blueprint=nationBlue)


@nationBlue.route("/nation/queryNationByName", methods=["POST", "GET"])
def queryNationByName():
    name = request.form.get('name')
    nations = Nation.query.filter(Nation.name == name).all()
    num = len(nations)
    if (num > 0):
        data={}
        fileId=nations[0].fileId
        if(fileId is not None):
            img =  "http://127.0.0.1:5000/static/" + fileId +'.jpg'
            data['img']=img
        desc=nations[0].desc
        descUrl = "http://127.0.0.1:5000/detail.html?name="+name
        data['descUrl'] = descUrl
        data['desc'] = desc
    return make_response(jsonify(data))


@nationBlue.route("/nation/queryNationHtmlByName", methods=["POST", "GET"])
def queryNationHtmlByName():
    name = request.form.get('name')
    nations = Nation.query.filter(Nation.name == name).all()
    num = len(nations)
    data = {}
    if (num > 0):
        data['html'] = nations[0].html
        data['name'] = nations[0].name
    return make_response(jsonify(data))


@nationBlue.route("/nation/updateAllNationHtml", methods=["POST", "GET"])
def updateAllNationHtml():
    nations = Nation.query.filter().all()
    for nation in nations:
        url = "https://baike.baidu.com/item/" + nation.name
        html = getHtml(url)
        nation.html = html
        db.session.add(nation)
        db.session.commit()
    return "success"


def getHtml(uri):
    # print(uri)
    # uri = "https://baike.baidu.com/item/%E8%97%8F%E6%97%8F"
    # url = "https://www.jianshu.com/p/19f631cbb21a"
    # ssl._create_default_https_context = ssl._create_unverified_context
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "BIDUPSID=E5228CF34864B67A8DA9188B3C1B67E4; PSTM=1556878941; BAIDUID=7E75138587824AE0719A5EEAF479B452:FG=1; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1558257118,1558622336,1558968701,1559051114; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1559051114; pgv_pvi=9893570560; pgv_si=s9041472512",
        "Host": "baike.baidu.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    res = requests.get(uri, headers=headers, allow_redirects=False, timeout=10).content.decode("utf-8")
    resSoup = BeautifulSoup(res, 'html.parser')
    div = resSoup.find_all(name='div', attrs={"class": "para"})
    html = ""
    for info in div:
        html += info.text
    return html


@nationBlue.route("/nation/queryAll", methods=["POST", "GET"])
def queryAll():
    nations = Nation.query.filter().all()
    nationDistributedInfo=[]
    for nation in nations:
        distributeds = Distributed.query.filter(Distributed.nationId==nation.name).all()
        nationJson={}
        nationJson['nationName']=nation.name
        nationInfos = []
        for distributed in distributeds:
            nationInfo={}
            value=[]
            # distributed.population
            value.append(distributed.longitude)
            value.append(distributed.latitude)
            value.append(getPerson(nation, distributeds))
            nationInfo['name'] = distributed.city
            nationInfo['value']=value
            nationInfo['province'] = distributed.province
            nationInfos.append(nationInfo)
        nationJson['data']=nationInfos
        nationDistributedInfo.append(nationJson)

    res={}
    res['nationDistributedInfo']=nationDistributedInfo
    return make_response(jsonify(res))


# 计算少数民族人数
def getPerson(nation, distributeds):
    population = nation.population
    num = len(distributeds)
    return int(population / num)

@nationBlue.route("/nation/createTable", methods=["POST", "GET"])
def createTable():
    db.drop_all()
    db.create_all()
    return "succ"


@nationBlue.route("/nation/spider", methods=["POST", "GET"])
def spider():
    nations = Nation.query.filter().all()
    url = "https://jingyan.baidu.com/article/4f7d5712b1c07c1a20192736.html"
    res = requests.get(url).content.decode("utf-8")
    resSoup = BeautifulSoup(res)
    div = resSoup.find_all(name='div', attrs={"class": "exp-content-body"})
    contents = div[1].contents[0].contents
    for content in contents:
        detail = content.contents[1].text
        for nation in nations:
            if (detail.count(nation.name) > 0):
                nation.desc = detail
                print(detail)
                img = content.contents[2].contents[0].contents[0].contents[0]
                url = img.attrs["data-src"]
                response = requests.get(url)
                img = response.content
                fileId = uuid.uuid1().__str__()
                print(url)
                print(fileId)
                nation.fileId = fileId
                time.sleep(5)
                base_dir = os.path.dirname(__file__)
                upload_path=os.path.join(base_dir,"data/pic/"+fileId+".jpg")
                with open(upload_path, 'wb') as f:
                    f.write(img)
                    f.close()
                db.session.add(nation)
                db.session.commit()



@nationBlue.route('/download/<string:fileId>', methods=['GET'])
def download(fileId):
    if request.method == "GET":
        base_dir = os.path.dirname(__file__)
        upload_path = os.path.join(base_dir, "data/pic/" )
        return send_from_directory("data/pic/", fileId+".jpg", as_attachment=True)

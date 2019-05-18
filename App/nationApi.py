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
nationBlue = Blueprint("nation", __name__)
import os

def init_nationBlue(app):
    app.register_blueprint(blueprint=nationBlue)


@nationBlue.route("/nation/queryNationByName", methods=["POST", "GET"])
def queryNationByName():
    name = request.form.get('name')
    nations = Nation.query.filter(Nation.name == name).all()
    num = len(nations)
    res = {}
    if (num > 0):
        res["data"] = nations[0].to_json()
    return make_response(jsonify(res))

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
            distributed.population
            value.append(distributed.longitude)
            value.append(distributed.latitude)
            value.append(getPerson(nation, distributeds))
            nationInfo['name'] = distributed.city
            nationInfo['value']=value
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

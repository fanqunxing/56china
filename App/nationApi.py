from flask import make_response
from App.common.ResData import ResData
from flask import Blueprint, request, jsonify, make_response, session
from App.Models import Nation,Distributed
from App.ext import db

nationBlue = Blueprint("nation", __name__)



def init_nationBlue(app):
    app.register_blueprint(blueprint=nationBlue)

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
            value.append('1111')
            nationInfo['name'] = distributed.city
            nationInfo['value']=value
            nationInfos.append(nationInfo)
        nationJson['data']=nationInfos
        nationDistributedInfo.append(nationJson)

    res={}
    res['nationDistributedInfo']=nationDistributedInfo
    return make_response(jsonify(res))



@nationBlue.route("/nation/createTable", methods=["POST", "GET"])
def createTable():
    db.drop_all()
    db.create_all()
    return "succ"
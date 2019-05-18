from flask import Blueprint, request,jsonify,make_response,session

from App.common.ResData import ResData
from App.ext import db
import  operator

blue =Blueprint("user",__name__)

def init_blue(app):
    app.register_blueprint(blueprint=blue)

@blue.route("/user/login",methods=["POST"])
def login():
    userName=request.form.get('userName')
    password=request.form.get('password')

    res.set_cookie('username', userName)
    return res







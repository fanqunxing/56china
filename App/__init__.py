from flask import Flask

from App.web import init_webBlue
from App.UserApi import init_blue
from App.ext import init_ext
from App.settings import envs


def create_app():
    app = Flask(__name__)

    app.config.from_object(envs.get('dev'))

    init_blue(app)
    init_webBlue(app)
    init_ext(app)

    return app


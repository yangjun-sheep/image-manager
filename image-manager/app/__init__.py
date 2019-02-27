# coding:utf8

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config
from common.logger import Logger

db = SQLAlchemy()


def init_logger(app):
    log_name = 'app'
    app.config['JSON_AS_ASCII'] = False
    log_level = app.config['LOG_LEVEL']
    log_file = app.config['LOG_FILE_CONFIG']['app']
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    app.logger = Logger(log_name, log_level, log_file).get_logger()


def init_static_dir(app):
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])


def create_app(config_name):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    init_logger(app)
    init_static_dir(app)

    from app.apis import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.apis import image_bp
    app.register_blueprint(image_bp, url_prefix='/api')

    return app

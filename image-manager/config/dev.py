# coding:utf8

from config.common import CommonConfig


class DevelopmentConfig(CommonConfig):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}:{port}/{db}'.format(
        user='root',
        password='huiying',
        host='127.0.0.1',
        port='3306',
        db='image_manager'
    )

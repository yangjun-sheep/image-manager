# coding:utf8

from config.common import CommonConfig


class ProductionConfig(CommonConfig):

    DEBUG = False

    API_HOST = 'http://a.shuaibaobao.vip'
    UPLOAD_FOLDER = '/www/wwwroot/bizhi/static/images'
    LOG_FILE_CONFIG = {
        'app': '/www/wwwroot/bizhi/logs/server.log',
    }

    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}:{port}/{db}'.format(
        user='a_shuaibaobao_vi',
        password='CErDJhdmmtJazRLh',
        host='127.0.0.1',
        port='3306',
        db='a_shuaibaobao_vi'
    )

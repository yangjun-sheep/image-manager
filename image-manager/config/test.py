# coding:utf8

from config.common import CommonConfig


class TestingConfig(CommonConfig):

    DEBUG = True
    
    API_HOST = 'http://a.shuaibaobao.vip'

    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{password}@{host}:{port}/{db}'.format(
        user='a_shuaibaobao_vi',
        password='CErDJhdmmtJazRLh',
        host='127.0.0.1',
        port='3306',
        db='a_shuaibaobao_vi'
    )

# coding:utf8


class CommonConfig(object):

    @staticmethod
    def init_app(app):
        pass

    UPLOAD_FOLDER = 'static/images'

    PAGE_SIZE = 20

    LOG_LEVEL = 'DEBUG'
    LOG_FILE_CONFIG = {
        'app': 'logs/server.log',
    }

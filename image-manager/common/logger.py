# coding:utf8

import logging
import logging.config


class Logger(object):

    def __init__(self, name, level, log_path):
        self.name = name
        self.level = level
        self.log_path = log_path
        self.logger_settings()
        self.other_module_settings()

    def get_logger(self):
        logger = logging.getLogger(self.name)
        return logger

    def logger_settings(self):
        config = {
            'version': 1,
            'disable_existing_loggers': True,

            'formatters': {
                'verbose': {
                    'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'simple': {
                    'format': '%(levelname)s %(message)s'
                },
            },

            'handlers': {
                'null': {
                    'level': 'DEBUG',
                    'class': 'logging.NullHandler',
                },
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose'
                },
                'file': {
                    'level': self.level,
                    'class': 'cloghandler.ConcurrentRotatingFileHandler',
                    'maxBytes': 1024 * 1024 * 50,
                    'backupCount': 50,
                    'delay': True,
                    'filename': self.log_path,
                    'formatter': 'verbose'
                    }
            },
            'loggers': {
                '': {
                    'handlers': ['file', 'console'],
                    'level': self.level,
                },
            }
        }
        logging.config.dictConfig(config)

    def other_module_settings(self):
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('pika').setLevel(logging.WARNING)

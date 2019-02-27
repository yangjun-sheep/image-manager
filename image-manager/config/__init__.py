from config.dev import DevelopmentConfig
from config.test import TestingConfig
from config.prod import ProductionConfig

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

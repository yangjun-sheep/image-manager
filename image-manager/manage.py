import os
from flask_script import Manager
from app import create_app

env = os.getenv('PYTHON_ENV', 'development')
env = 'production'


app = create_app(env)
manager = Manager(app)


if __name__ == '__main__':
    manager.run()

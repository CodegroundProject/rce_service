# encoding: utf-8
# from flask_script import Manager

from project.app import create_app
from project.routes import rce

app = create_app()

app.register_blueprint(rce)
# manager = Manager(app)

if __name__ == '__main__':
    app.run()

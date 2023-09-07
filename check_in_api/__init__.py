from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8fa0dfae52e41baf92b776e6a986724e287602d18092146f90735f2567356734'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

api = Api(app)

from check_in_api.api_resources import Test
api.add_resource(Test,'/test','/test/')
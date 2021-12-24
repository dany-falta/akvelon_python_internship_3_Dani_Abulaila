from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api, Resource
from flask_marshmallow import Marshmallow
from financial_app.utils import fibonacci

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app,
        title='Akvelon REST API',
        description='A REST API for storing user and transactions information')
ma = Marshmallow(app)

@api.route('/fibonacci/<int:n>')
class Fibonacci(Resource):
    def get(self, n):
        return fibonacci(n), 200

from financial_app.user.routes import api as ns1
from financial_app.finance.routes import api as ns2
api.add_namespace(ns1, path='/user')
api.add_namespace(ns2, path='/finance')

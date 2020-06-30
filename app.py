from flask import Flask,jsonify
from flask_restful import Api
from marshmallow import ValidationError
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv

from db import db
from ma import ma
from resources.exchange import Exchange
from resources.deposit import Deposit
from resources.cryptocurrency import Cryptocurrency
from resources.trade import Trade,TradeList



app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(Exchange, '/api/v1/crypto/exchanges')
api.add_resource(Deposit, '/api/v1/crypto/exchanges/<int:exchange_id>')
api.add_resource(Cryptocurrency, '/api/v1/crypto/exchanges/<int:exchange_id>/currencie')
api.add_resource(Trade, '/api/v1/crypto/exchanges/<int:exchange_id>/trades')
api.add_resource(TradeList, '/api/v1/crypto/history')


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, )

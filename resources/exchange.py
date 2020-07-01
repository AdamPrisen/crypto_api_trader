from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from models.exchange import ExchangeModel
from schemas.exchange import ExchangeSchema
from libs.strings import gettext

exchange_schema= ExchangeSchema()

class Exchange(Resource):
    @classmethod
    def post(cls):

        exchange_json = request.get_json()
        exchange = exchange_schema.load(exchange_json)
        
        if ExchangeModel.find_by_name(exchange.name):
            return {"message": gettext("exchange_name_exists").format(exchange.name)}, 400
        
        try:
            exchange.save_to_db()
        except:
            return {"message": gettext("exchange_inserting_error")}, 500

        return exchange_schema.dump(exchange), 201
        
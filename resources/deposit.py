from libs.strings import gettext
from schemas.deposit import DepositSchema
from models.exchange import ExchangeModel
from flask import request
from flask_restful import Resource

deposit_schema = DepositSchema()


class Deposit(Resource):
    @classmethod
    def post(cls, exchange_id):
        deposit_json = request.get_json()
        deposit = deposit_schema.load(deposit_json)
        exchange = ExchangeModel.find_by_id(exchange_id)
        if exchange is None:
            return {"message": gettext("exchange_id_not_exists").format(exchange_id)}
        try:
            exchange.change_amount(deposit['amount'])
        except:
            return {"message": gettext("exchange_deposit_error")}, 500

        return 200
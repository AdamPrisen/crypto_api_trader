from flask_restful import Resource
from flask import request, jsonify
from models.trade import TradeModel
from models.exchange import ExchangeModel
from schemas.trade import TradeSchema
from libs.strings import gettext

trade_schema = TradeSchema()
trade_list_schema = TradeSchema(many=True)


class Trade(Resource):
    @classmethod
    def post(cls, exchange_id: int):
        trade_json = request.get_json()
        trade_json['exchange_id'] = exchange_id
        trade = trade_schema.load(trade_json)
        exchange = ExchangeModel.find_by_id(exchange_id)

        #Checking if exchange exists
        if exchange is None:
            return {"message": gettext('exchange_id_not_exists').format(exchange_id)}, 400
        
        #set and check currency in
        if trade.currency_in == exchange.currency:
            currency_in = exchange
        else:
            currency_in = exchange.find_currency_by_shortcut(trade.currency_in)
            if currency_in is None:
                return {"message": gettext("currency_not_exists").format(trade.currency_in)}, 400
        if trade.amount > currency_in.amount:
            return {"message": gettext("lack_of_resources").format(
                currency_in.amount,trade.currency_in
            )}, 400

        #set and check currency out
        if trade.currency_out == exchange.currency:
            currency_out = exchange
        else:
            currency_out = exchange.find_currency_by_shortcut(trade.currency_out)
            if currency_out is None:
                return {"message": gettext("currency_not_exists").format(trade.currency_out)}, 400

        #transfer amount
        try:
            currency_in.amount -= trade.amount
            currency_out.amount += trade.amount*currency_in.rate/currency_out.rate
            currency_in.save_to_db()
            currency_out.save_to_db()
            trade.save_to_db()
        except:
            return{"message": gettext("trade_error")},500

        return{"message": gettext('trade_success').format(trade.amount,trade.currency_in)},201


class TradeList(Resource):

    @classmethod
    def get(cls):
        return{"trades": trade_list_schema.dump(TradeModel.trade_filter(request.args.to_dict()))}


 
 

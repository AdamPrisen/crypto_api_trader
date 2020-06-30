from ma import ma

from models.cryptocurrency import CryptocurrencyModel
from models.exchange import ExchangeModel
from schemas.trade import TradeSchema
from schemas.cryptocurrency import CryptocurrencySchema
from marshmallow import fields, validate



class ExchangeSchema(ma.SQLAlchemyAutoSchema):
    trades = ma.Nested(TradeSchema, many=True)
    cryptocurrencies = ma.Nested(CryptocurrencySchema, many=True)
    class Meta:
        model = ExchangeModel
        dump_only = ("id","amount")
        load_instance = True
    name = fields.String(required=True, validate=[validate.Length(min=1)])
    currency = fields.String(required=True, validate=[validate.Length(min=3)])


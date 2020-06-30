from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from models.cryptocurrency import CryptocurrencyModel
from schemas.cryptocurrency import CryptocurrencySchema
from libs.strings import gettext

currency_schema = CryptocurrencySchema()
currency_list_schema = CryptocurrencySchema(many=True)

class Cryptocurrency(Resource):
    @classmethod
    def put(cls,exchange_id: int ):
        currency_json = request.get_json()
        currency_json['exchange_id'] = exchange_id

        if 'shortcut' not in currency_json:
            return {"message": gettext("currency_shortcut_required")}
        currency = CryptocurrencyModel.find_by_shortcut(
            currency_json['shortcut'],
            exchange_id
        )
        
        #delete
        if 'delete' in currency_json:
                if currency is None:
                    return {"message": gettext(
                        'currency_not_exists'
                        ).format(currency_json['shortcut'])},400
                try:
                    currency.delete_from_db()
                except:
                    return{"message": gettext("cryptocurrency_updating_error")}, 500
                
                return {'cryptocurrencies': currency_list_schema.dump(
                        CryptocurrencyModel.find_all_in_exchange(exchange_id)
                        )}, 200
            
        #create new
        if currency is None:
                currency = currency_schema.load(currency_json)
        #update 
        else:
            currency = currency_schema.load(currency_json, instance=currency, partial=True)
        try: 
            currency.save_to_db()
        except: 
            return{"message": gettext("cryptocurrency_updating_error")},500

        return {'cryptocurrencies':currency_list_schema.dump(
                    CryptocurrencyModel.find_all_in_exchange(exchange_id)
            )}, 201
        
        
        

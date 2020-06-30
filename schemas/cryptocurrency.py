from ma import ma
from libs.strings import gettext
from models.cryptocurrency import CryptocurrencyModel
from marshmallow import Schema, fields, validate, validates, ValidationError


class CryptocurrencySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CryptocurrencyModel
        dump_only = ("id","amount","delete")
        load_instance = True
        include_fk = True
    shortcut = fields.Str(required=True, validate=[validate.Length(min=3)])
    rate = fields.Float(required=True)

    @validates('rate')
    def validate_numbers(self,value):
        if value <= 0:
            raise ValidationError(gettext("rate_above_zero"))
    

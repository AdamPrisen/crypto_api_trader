from ma import ma
from models.trade import TradeModel
from marshmallow import validates, ValidationError
from libs.strings import gettext




class TradeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TradeModel
        dump_only = ("id",'created_date')
        load_instance = True
        include_fk = True
    
    @validates('amount')
    def is_amount_above_zero(self, value):
        if value <= 0:
            raise ValidationError(gettext("trade_amount_above_zero"))

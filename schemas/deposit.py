from libs.strings import gettext
from marshmallow import Schema, fields, validates, ValidationError

class DepositSchema(Schema):
    amount = fields.Float()

    @validates('amount')
    def is_amount_above_zero(self, value):
        if value <= 0:
            raise ValidationError(gettext("rate_above_zero"))


from db import db
import datetime
from sqlalchemy import or_
from werkzeug.exceptions import BadRequest, InternalServerError
from libs.strings import gettext


class TradeModel(db.Model):

    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(precision=5), nullable=False)
    currency_in = db.Column(db.String(10), nullable=False)
    currency_out = db.Column(db.String(10), nullable=False)
    created_date = db.Column(db.DateTime(timezone=True),server_default=db.func.current_timestamp())
    exchange_id = db.Column(db.Integer, db.ForeignKey('exchanges.id'), nullable=False)
    exchange = db.relationship('ExchangeModel')


    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def change_amount(self, amount):
        self.amount += amount
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
     #filters:
    @classmethod
    def trade_filter(cls,filters,offset=0,limit=10):
        query = cls.query
        if 'offset' in filters:
            try: 
                offset = filters['offset']
                int(offset)
            except:
                raise BadRequest(gettext("invalid_offset"))

        if 'limit' in filters:
            try:
                limit = filters['limit']
                int(limit)
            except:
                BadRequest(gettext("invalid_limit"))

        if 'exchange_id' in filters:
            query = query.filter_by(exchange_id=filters['exchange_id'])

        if 'search' in filters:
            query = query.filter(
                or_(cls.currency_in.like(filters['search']),cls.currency_out.like(filters['search']))
            )

        if 'date_from' in filters:
            try:
                date_from = datetime.datetime.strptime(filters['date_from'], '%Y-%m-%dT%H:%M:%S')
            except:
                raise BadRequest(gettext("invalid_date"))
            query = query.filter(cls.created_date>=date_from)

        if 'date_to' in filters:
            try:
                date_to = datetime.datetime.strptime(filters['date_to'], '%Y-%m-%dT%H:%M:%S')
            except:
                raise BadRequest(gettext("invalid_date"))
            query = query.filter(cls.created_date<=date_to)

        #try:
        return query.order_by(cls.created_date.desc()).offset(offset).limit(limit).all()
        #except:
           # raise InternalServerError(gettext('trades_error'))



from db import db


class ExchangeModel(db.Model):

    __tablename__ = 'exchanges'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    amount = db.Column(db.Float(precision=2), default=0)
    currency = db.Column(db.String(10), nullable=False)
    cryptocurrencies = db.relationship('CryptocurrencyModel', lazy='dynamic')
    trades = db.relationship('TradeModel')

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    def find_currency_by_shortcut(self, shortcut):
        return self.cryptocurrencies.filter_by(shortcut=shortcut).first()
    

    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @property
    def rate(self):
        return 1
    
    def change_amount(self, amount): 
        self.amount += amount
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    

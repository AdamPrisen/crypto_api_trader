from db import db


class CryptocurrencyModel(db.Model):

    __tablename__ = 'cryptocurrencies'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(precision=5), default=0)
    rate = db.Column(db.Float(precision=5), nullable=False)
    shortcut = db.Column(db.String(10), nullable=False)
    exchange_id = db.Column(db.Integer, db.ForeignKey('exchanges.id'), nullable=False)
    exchange = db.relationship('ExchangeModel')




    @classmethod
    def find_by_shortcut(cls, shortcut: str, exchange_id: int):
        return cls.query.filter_by(shortcut=shortcut, exchange_id=exchange_id).first()

    @classmethod
    def find_all_in_exchange(cls, exchange_id):
        return cls.query.filter_by(exchange_id=exchange_id).all()

    def change_amount(self, amount):
        self.amount += amount
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

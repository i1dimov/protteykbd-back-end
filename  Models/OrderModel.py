from dataclasses import dataclass
from app import db


@dataclass
class Order(db.Model):
    id: int
    user_id: int
    cart_id: int
    status: str
    address: str
    price: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), unique=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('Cart.id'))
    status = db.Column(db.String(20))
    address = db.Column(db.String)
    price = db.Column(db.Integer)

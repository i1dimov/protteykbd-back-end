from dataclasses import dataclass

from app import db


@dataclass
class Item(db.Model):
    id: int
    name: str
    description: str
    image: str
    price: int
    quantity: int
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True, unique=False)
    image = db.Column(db.String(20))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
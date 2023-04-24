from dataclasses import dataclass

from app import db


@dataclass
class Wishlist(db.Model):
    id: int
    user_id: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), unique=True)
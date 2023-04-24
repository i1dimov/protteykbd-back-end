from dataclasses import dataclass

from app import db


@dataclass
class WishlistItem(db.Model):
    id: int
    item_id: int
    quantity: int
    cart_id: int
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('Item.id'))
    quantity = db.Column(db.Integer)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('Wishlist.id'))
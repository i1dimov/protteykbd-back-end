from app import db
from dataclasses import dataclass


# Entity
@dataclass
class User(db.Model):
    id: int
    login: str
    password: str
    cart_id: int
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('cart.id'), unique=True)

    def __repr__(self):
        return f"<user {self.id}>"


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
    image = db.Column(db.LargeBinary)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return f"<item {self.id}>"


@dataclass
class Cart(db.Model):
    id: int
    user_id: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    def __repr__(self):
        return f"<cart {self.id}>"


@dataclass
class CartItem(db.Model):
    id: int
    item_id: int
    item_type: str
    quantity: int
    cart_id: int
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item_type = db.Column(db.String(20))  # Keyboard, Constructor
    quantity = db.Column(db.Integer)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))

    def __repr__(self):
        return f"<cartItem {self.id}>"


@dataclass
class Wishlist(db.Model):
    id: int
    user_id: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    def __repr__(self):
        return f"<wishlist {self.id}>"


@dataclass
class WishlistItem(db.Model):
    id: int
    item_id: int
    quantity: int
    wishlist_id: int
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantity = db.Column(db.Integer)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlist.id'))

    def __repr__(self):
        return f"<wishlistItem {self.id}>"


@dataclass
class Order(db.Model):
    id: int
    user_id: int
    cart_id: int
    status: str
    address: str
    price: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    status = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)

    def __repr__(self):
        return f"<order {self.id}>"


@dataclass
class Constructor(db.Model):
    id: int
    user_id: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    def __repr__(self):
        return f"<constructor {self.id}>"


@dataclass
class ConstructorItem(db.Model):
    id: int
    constructor_id: int
    component_id: int
    id = db.Column(db.Integer, primary_key=True)
    constructor_id = db.Column(db.Integer, db.ForeignKey('constructor.id'))
    component_id = db.Column(db.Integer, db.ForeignKey('component.id'))

    def __repr__(self):
        return f"<constructor {self.id}>"


@dataclass
class Component(db.Model):
    id: int
    type: str  # stabilizer, kit, pcb, case, switches...
    size: str  # 65%, 75%, 100%...
    mount: str  # tray, gasket...
    connector: str  # none, left type-c, right type-c, center type-c...
    stabilizers: str  # screw in, plate mount...
    layout: str  # ANSI/ISO
    price: float
    link: str
    image: str
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    size = db.Column(db.String)
    mount = db.Column(db.String)
    connector = db.Column(db.String)
    stabilizers = db.Column(db.String)
    layout = db.Column(db.String)
    price = db.Column(db.Float)
    link = db.Column(db.String)
    image = db.Column(db.LargeBinary)

    def __repr__(self):
        return f"<component {self.id}>"

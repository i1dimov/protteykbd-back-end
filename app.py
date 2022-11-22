from flask import Flask, json, jsonify, request
from flask_cors import CORS
from dataclasses import dataclass
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'impossible_to_hack'
db = SQLAlchemy(app)
CORS(app)


# Entity
@dataclass
class User(db.Model):
    id: int
    login: str
    password: str
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


@dataclass
class Product(db.Model):
    id: int
    name: str
    description: str
    images: str
    price: int
    quantity: int
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True, unique=False)
    images = db.Column(db.String(20))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)


@dataclass
class Cart(db.Model):
    id: int
    user_id: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), unique=True)


@dataclass
class CartItem(db.Model):
    id: int
    product_id: int
    quantity: int
    cart_id: int
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'))
    quantity = db.Column(db.Integer)
    cart_id = db.Column(db.Integer, db.ForeignKey('Cart.id'))


@dataclass
class Wishlist(db.Model):
    id: int
    user_id: int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), unique=True)


@dataclass
class WishlistItem(db.Model):
    id: int
    product_id: int
    quantity: int
    cart_id: int
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'))
    quantity = db.Column(db.Integer)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('Wishlist.id'))


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


# Routes

# Home
@app.route('/')
def index():
    return "sweet home"


# Login
@app.route('/login')
def login():
    return "login"


# Register
@app.route("/register")
def register():
    return "register"


# Product
@app.route("/product")
def product():
    return "product"



if __name__ == "__main__":
    app.run(debug=True)

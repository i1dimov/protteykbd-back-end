from flask import Flask, jsonify, request, render_template, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dataclasses import dataclass
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from imagekitio import ImageKit
from models import *
import redis
from flask_session import Session
from component_price_parser import get_price

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asdfhasdhf93408932i4uh08723fi0hadsf0813u4r'

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url("redis://127.0.0.1:6379")

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()


imagekit = ImageKit(
    public_key='public_F1jpuG3pmF8Or4l1zVdWkCQSNHI=',
    private_key='private_EZXS35qhxnj0HQnXAuOQYWsha9U=',
    url_endpoint='https://ik.imagekit.io/xiultnofr'
)


@app.route('/upload', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return 'no image', 400

        itemName = secure_filename(file.filename)
        upload = imagekit.upload_file(
            file=file,
            file_name=itemName
        )
        return upload.response_metadata.raw
    return render_template('upload.html')


# Login
@app.route('/login', methods=['POST'])
def login():
    login = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(login=login).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    session['user_id'] = user.id
    return jsonify({
        "id": user.id,
        "email": user.login
    }), 200


# Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop("user_id")
    return 'User logged out', 200


# User
@app.route('/user')
def current_user():
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.login
    }), 200


# Register
@app.route("/register", methods=['POST'])
def register():
    login = request.json['email']
    password = request.json['password']
    user_exists = User.query.filter_by(login=login).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409
    hashed_password = bcrypt.generate_password_hash(password)
    user_count = len(User.query.all())
    cart_count = len(Cart.query.all())
    new_user = User(login=login, password=hashed_password, cart_id=cart_count+1)
    new_cart = Cart(user_id=user_count+1)
    new_wishlist = Wishlist(user_id=user_count+1)
    db.session.add(new_user)
    db.session.add(new_cart)
    db.session.add(new_wishlist)
    db.session.commit()
    return jsonify({
        "id": new_user.id,
        "email": new_user.login
    })


# Item
# получить информацию об отдельном товаре
@app.route("/item/<item_id>")
def item(item_id):
    if request.method == 'GET':
        item = Item.query.filter(Item.id == item_id).first()
        return jsonify(item)


@app.route("/items")
def items():
    if request.method == 'GET':
        items = Item.query.all()
        return jsonify(items)


# Cart
# Добавить или удалить из корзины, получить данные о корзине
@app.route('/cart', methods=['GET', 'POST', 'DELETE'])
def cart():
    if request.method == 'GET':
        cart = Cart.query.filter(Cart.user_id == session.get("user_id")).first()
        cart_items = CartItem.query.filter(CartItem.cart_id == cart.id).all()
        return jsonify(cart_items)
    if request.method == 'POST':
        item_id = request.json['item_id']
        item_type = request.json['item_type']
        quantity = request.json['quantity']
        cart_id = User.query.filter(User.id == session.get("user_id")).first().cart_id
        cart_item = CartItem(item_id=item_id, quantity=quantity, item_type=item_type, cart_id=cart_id)
        db.session.add(cart_item)
        db.session.commit()
        return '200'
    if request.method == 'DELETE':
        item_id = request.json['item_id']
        cart_id = User.query.get(session.get("user_id")).cart_id
        cart_item = CartItem.query.filter(CartItem.cart_id == cart_id, CartItem.item_id == item_id).first()
        db.session.delete(cart_item)
        db.session.commit()
        return '200'


# Wishlist
@app.route('/wishlist', methods=['GET', 'POST', 'DELETE'])
def wishlist():
    if request.method == 'GET':
        wishlist = Wishlist.query.filter(Wishlist.id == session.get("user_id")).first()
        wishlist_items = WishlistItem.query.filter(wishlist.id).all()
        return jsonify(wishlist_items)
    if request.method == 'POST':
        item_id = request.json['item_id']
        quantity = request.json['quantity']
        wishlist_id = session.get("user_id")
        wishlist_item = WishlistItem(item_id=item_id, quantity=quantity, wishlist_id=wishlist_id)
        db.session.add(wishlist_item)
        db.session.commit()
        return '200'
    if request.method == 'DELETE':
        item_id = request.json['item_id']
        wishlist_id = session.get("user_id")
        wishlist_item = WishlistItem.query.filter(wishlist_id == wishlist_id, item_id == item_id).first()
        db.session.delete(wishlist_item)
        db.session.commit()
        return '200'


# Orders
# Получить заказы текущего пользователя
@app.route('/orders', methods=['GET'])
def orders():
    user_id = session.get("user_id")
    orders = Order.query.filter(Order.user_id == user_id)
    return jsonify(orders)


# Конструктор
# Получить все запчасти, добавить в корзину
@app.route('/constructor', methods=['GET', 'POST', 'DELETE'])
def constructor():
    constructor = Constructor.get(Constructor.user_id == session.get("user_id"))
    if request.method == 'GET':
        components = Component.query.all()
        return jsonify(components)
    if request.method == 'POST':
        components = request.json['components']
        for component in components:
            new_component = ConstructorItem(component_id=component.id, constructor_id=constructor.id)
            db.session.add(new_component)
        db.session.commit()
        return '200'
    if request.method == 'DELETE':
        components = request.json['components']
        for component in components:
            delete_component = ConstructorItem(component_id=component.id, constructor_id=constructor.id)
            db.session.delete(delete_component)
        db.session.commit()
        return '200'


if __name__ == "__main__":
    app.run(debug=True)

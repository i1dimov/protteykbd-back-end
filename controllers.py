from flask import json, jsonify, request
from flask_cors import CORS
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import app


# Routes

# Home
from models import *
from app import db


@app.route('/')
def index():
    # GET - получить все товары
    return "sweet home"


# Login
@app.route('/login')
def login():
    return "login"


# Register
@app.route("/register")
def register():
    return "register"


# Item
# получить информацию об отдельном товаре
@app.route("/item/<itemID>", methods=['POST', 'GET', 'DELETE'])
@app.route("/item/")
def item(itemID):
    if request.method == 'GET':
        item = Item.query.filter(Item.id == itemID)
        return jsonify(item)

    if request.method == 'POST':
        newItem = request.get_json(force=True)
        item = Item(
            name=newItem['name'],
            description=newItem['description'],
            image=newItem['image'],
            price=newItem['price'],
            quantity=newItem['quantity'])
        try:
            db.session.add(item)
            db.session.commit()
            return jsonify(newItem)
        except sqlite3.Error as e:
            return "При создании товара произошла ошибка: " + str(e)


@app.route("/item")
def items():
    return "item"


# Cart
# Добавить или удалить из корзины, получить данные о корзине
@app.route('/cart')
def cart():
    return "cart"


# Wishlist
# Позже
@app.route('/wishlist')
def wishlist():
    return "wishlist"


# Orders
# Получить заказы текущего пользователя
@app.route('/orders')
def cart():
    return "orders"


# Конструктор
# Получить все запчасти, добавить в корзину
@app.route('/constructor')
def constructor():
    return "orders"

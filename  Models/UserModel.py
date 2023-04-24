# Entity
from dataclasses import dataclass

from app import db


@dataclass
class User(db.Model):
    id: int
    login: str
    password: str
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
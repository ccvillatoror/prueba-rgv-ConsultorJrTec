from db import db
from flask_login import UserMixin


class Usuarios(db.Model, UserMixin):
    id = db.Column('idusuario', db.Integer, primary_key=True, nullable=False)
    usuario = db.Column('usuario', db.String(20), unique=True, nullable=False)
    contraseña = db.Column('contraseña', db.String(180), nullable=False)

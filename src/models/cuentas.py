from db import db

class Cuentas(db.Model):
    id = db.Column('idcuenta', db.Integer, primary_key=True, nullable=False)
    saldo = db.Column('saldo', db.Float, nullable=False)
    pagos = db.relationship('Pagos')


    def __init__(self, saldo):
            self.saldo = saldo

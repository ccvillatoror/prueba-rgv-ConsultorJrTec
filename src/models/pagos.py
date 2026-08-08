import datetime
from db import db


class Pagos(db.Model):
    id = db.Column('idPago', db.Integer, primary_key=True, nullable=False)
    fecha = db.Column('fechaPago', db.DateTime, nullable=False, default=datetime.date.today)
    id_gasto = db.Column('idGasto', db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
    cuenta = db.Column('columnaAsociada', db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
    monto_pagado = db.Column('montoPagado', db.Float, nullable=False)
    estado = db.Column('estado', db.String(10), nullable=False, default='En proceso')

    def __init__(self, fecha, id_gasto, cuenta, monto_pagado):
            self.fecha = fecha
            self.id_gasto = id_gasto
            self.cuenta = cuenta
            self.monto_pagado = monto_pagado
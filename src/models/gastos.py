import datetime
from db import db


class Gastos(db.Model):
    id = db.Column('idgasto', db.Integer, primary_key=True, nullable=False)
    fecha = db.Column('fechagasto', db.DateTime, nullable=False, default=datetime.date.today)
    concepto = db.Column('concepto', db.String(100), nullable=False)
    monto_gastado = db.Column('montogastado', db.Float, nullable=False)
    estado = db.Column('estado', db.String(10), nullable=False, default='En proceso')
    monto_pagado = db.Column('montopagado', db.Float, nullable=False, default=0.0)
    pagos = db.relationship('Pagos', backref='gasto', lazy=True)

    def to_dict(self):
            return {
                'id': self.id,
                'fecha': self.fecha,
                'concepto': self.concepto,
                'monto_gastado': self.monto_gastado,
                'monto_pagado': self.monto_pagado,
                'saldo_pendiente': round(self.monto_gastado - self.monto_pagado, 2),
                'estado': self.estado,
            }

    def __init__(self, fecha, concepto, monto_gastado):
        self.fecha = fecha
        self.concepto = concepto
        self.monto_gastado = monto_gastado

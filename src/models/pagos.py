import datetime
from db import db


class Pagos(db.Model):
    __tablename__ = 'pagos'
    id = db.Column('idpago', db.Integer, primary_key=True, nullable=False)
    fecha = db.Column('fechapago', db.DateTime, nullable=False, default=datetime.date.today)
    id_gasto = db.Column('idgasto', db.Integer, db.ForeignKey('gastos.idgasto'), nullable=False)
    cuenta = db.Column('cuentaasociada', db.Integer, db.ForeignKey('cuentas.idcuenta'), nullable=False)
    monto_pagado = db.Column('montopagado', db.Float, nullable=False)
    estado = db.Column('estado', db.String(10), nullable=False, default='En proceso')

    def to_dict(self):
        return {
             'id': self.id,
             'fecha': self.fecha,
             'id_gasto': self.id_gasto,
             'cuenta': self.cuenta,
             'monto_pagado': self.monto_pagado,
             'estado': self.estado             
             }
    
    def __init__(self, fecha, id_gasto, cuenta, monto_pagado):
            self.fecha = fecha
            self.id_gasto = id_gasto
            self.cuenta = cuenta
            self.monto_pagado = monto_pagado
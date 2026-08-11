from functools import wraps

from db import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.cuentas import Cuentas
from models.gastos import Gastos
from models.pagos import Pagos
from models.usuarios import Usuarios
from werkzeug.security import check_password_hash

api_bp = Blueprint('api', __name__)

def api_requiere_autenticacion(f):
    @wraps(f)
    @jwt_required() # Para que Flask-JWT-Extended busque el token en las cabeceras automáticamente
    def decorador(*args, **kwargs):
        
        return f(*args, **kwargs)
    return decorador

@api_bp.route('/login', methods=['POST'])
def api_login():
    datos = request.get_json()
    
    if not datos:
        return jsonify({"error": "Se requieren datos en formato JSON"}), 400
        
    usr = datos.get('user')
    pwd = datos.get('password')

    usuario = db.session.execute(
        db.select(Usuarios).filter_by(usuario=usr)
    ).scalar_one_or_none()
    
    # Valida las credenciales
    if usuario and check_password_hash(usuario.contraseña, pwd):
        # Se crea el token JWT guardando la identidad del usuario
        token_acceso = create_access_token(identity=usuario.usuario)
        
        # Devuelve el token en un JSON con estado 200 (OK)
        return jsonify({
            "mensaje": "Ha ingresado correctamente",
            "token": token_acceso
        }), 200
        
    return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

@api_bp.route('/', methods=['GET'])
@api_requiere_autenticacion
def api_index():
    return jsonify({
        'recursos': {
            'gastos': '/api/gastos',
            'gasto_por_id': '/api/gastos/<id>',
            'pagos': '/api/pagos',
            'pago_por_id': '/api/pagos/<id>',
            'cuentas': '/api/cuentas',
            'cuenta_por_id': '/api/cuentas/<id>',
        },
        'autenticacion': 'HTTP Basic Auth (usuario y contraseña de la aplicación)',
        'filtros': {
            'gastos': '?estado=En proceso|Aprobado|Liquidado|Cancelado',
            'pagos': '?estado=En proceso|Aprobado|Cancelado',
        }
    })


@api_bp.route('/gastos/', methods=['GET'])
@api_bp.route('/gastos', methods=['GET'])
@api_requiere_autenticacion
def api_gastos():
    consulta = db.select(Gastos)

    estado = request.args.get('estado')
    if estado:
        consulta = consulta.where(Gastos.estado == estado)

    consulta = consulta.order_by(Gastos.id)

    gastos = db.session.execute(consulta).scalars().all()

    return jsonify([g.to_dict() for g in gastos])


@api_bp.route('/gastos/<int:gasto_id>', methods=['GET'])
@api_requiere_autenticacion
def api_gasto_detalle(gasto_id):
    gasto = db.session.get(Gastos, gasto_id)

    if not gasto:
        return jsonify({'error': f'No existe un gasto con id {gasto_id}.'}), 404

    return jsonify(gasto.to_dict())

@api_bp.route('/pagos/', methods=['GET'])
@api_bp.route('/pagos', methods=['GET'])
@api_requiere_autenticacion
def api_pagos():
    consulta = db.select(Pagos)

    estado = request.args.get('estado')
    if estado:
        consulta = consulta.where(Pagos.estado == estado)

    id_gasto = request.args.get('id_gasto', type=int)
    if id_gasto:
        consulta = consulta.where(Pagos.id_gasto == id_gasto)

    consulta = consulta.order_by(Pagos.id)

    pagos = db.session.execute(consulta).scalars().all()
    return jsonify([p.to_dict() for p in pagos])


@api_bp.route('/pagos/<int:pago_id>', methods=['GET'])
@api_requiere_autenticacion
def api_pago_detalle(pago_id):
    pago = db.session.get(Pagos, pago_id)

    if not pago:
        return jsonify({'error': f'No existe un pago con id {pago_id}.'}), 404

    return jsonify(pago.to_dict())

@api_bp.route('/cuentas/', methods=['GET'])
@api_bp.route('/cuentas', methods=['GET'])
@api_requiere_autenticacion
def api_cuentas():
    cuentas = db.session.execute(
        db.select(Cuentas).order_by(Cuentas.id)
    ).scalars().all()

    return jsonify([c.to_dict() for c in cuentas])


@api_bp.route('/cuentas/<int:cuenta_id>', methods=['GET'])
@api_requiere_autenticacion
def api_cuenta_detalle(cuenta_id):
    cuenta = db.session.get(Cuentas, cuenta_id)

    if not cuenta:
        return jsonify({'error': f'No existe una cuenta con id {cuenta_id}.'}), 404

    return jsonify(cuenta.to_dict())

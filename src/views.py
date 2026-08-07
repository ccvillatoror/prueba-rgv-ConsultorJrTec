from flask import Blueprint, render_template

view_bp = Blueprint('view', __name__)

@view_bp.route('/')
@view_bp.route('/home')
def home():
    return render_template('home.html')

@view_bp.route('/gastos')
def gastos():
    return render_template('ver_gastos.html')

@view_bp.route('/gastos/nuevo', methods=['GET', 'POST'])
def nuevo_gasto():
    return render_template('nuevo_gasto.html')

@view_bp.route('/pagos')
def pagos():
    return render_template('ver_pagos.html')

@view_bp.route('/pagos/nuevo')
def nuevo_pago():
    return render_template('nuevo_pago.html')

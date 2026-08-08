from flask import Blueprint, render_template, request, flash
from datetime import date 


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
    if request.method == 'POST':
        concepto = request.form.get('concepto-gasto')
        fecha = request.form.get('fecha-gasto')
        monto = request.form.get('monto-gasto')

        if len(concepto) < 6:
            flash('Instroduzca un concepto de más de 6 caracteres.', category='error')
        elif len(fecha) < 4:
            fecha = date.today().strftime("%d/%m/%Y")
            flash(f'El gasto fue guardado con fecha de hoy ({fecha}).', category='success')
        else:
            flash('Nuevo gasto registrado.', category='success')

    return render_template('nuevo_gasto.html')

@view_bp.route('/pagos')
def pagos():
    return render_template('ver_pagos.html')

@view_bp.route('/pagos/nuevo', methods=['GET', 'POST'])
def nuevo_pago():
    if request.method == 'POST':
        gasto = request.form.get('gasto-relacionado')
        monto = request.form.get('monto-gastado')
        cuenta = request.form.get('cuenta-asociada')
        fecha = request.form.get('fecha-pago')

        if len(fecha) < 4:
            fecha = date.today().strftime("%d/%m/%Y")
            flash(f'El pago fué guardado con fecha de hoy ({fecha}).', category='success')
        else:
            flash('Pago registrado.', category='success')


    return render_template('nuevo_pago.html')

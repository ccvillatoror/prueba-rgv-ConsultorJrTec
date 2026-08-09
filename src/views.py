from datetime import date
from db import db 
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from models.gastos import Gastos
from models.pagos import Pagos
from sqlalchemy.exc import InternalError

view_bp = Blueprint('views', __name__)

@view_bp.route('/')
@view_bp.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

@view_bp.route('/gastos/')
@view_bp.route('/gastos')
@login_required
def gastos():
    return render_template('ver_gastos.html', user=current_user)

@view_bp.route('/gastos/nuevo/', methods=['GET', 'POST'])
@view_bp.route('/gastos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_gasto():
    if request.method == 'POST':
        concepto = request.form.get('concepto-gasto')
        fecha = request.form.get('fecha-gasto')
        monto = request.form.get('monto-gasto')
        es_hoy = ''

        if len(fecha) < 1:
            fecha = date.today().strftime("%d/%m/%Y")
            es_hoy = 'de hoy '
        if len(concepto) < 6:
            flash('Instroduzca un concepto de más de 6 caracteres.', category='error')            
        else:
            try:
                # Agregarlo a la base de datos
                n_gasto = Gastos(fecha=fecha, concepto=concepto, monto_gastado=monto)
                db.session.add(n_gasto)
                db.session.commit()
            except InternalError as e:
                flash(str(e.orig).split('CONTEXT')[0])
                db.session.rollback()
                return render_template('nuevo_gasto.html', user=current_user)


            flash(f'El gasto fue guardado con fecha {es_hoy}{fecha}.', category='success')
            return redirect(url_for('views.gastos'))

        
            
    return render_template('nuevo_gasto.html', user=current_user)

@view_bp.route('/pagos/')
@view_bp.route('/pagos')
@login_required
def pagos():
    return render_template('ver_pagos.html', user=current_user)

@view_bp.route('/pagos/nuevo/', methods=['GET', 'POST'])
@view_bp.route('/pagos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_pago():
    if request.method == 'POST':
        gasto = request.form.get('gasto-relacionado')
        monto = request.form.get('monto-pagado')
        cuenta = request.form.get('cuenta-asociada')
        fecha = request.form.get('fecha-pago')
        es_hoy = ''

        if len(fecha) < 1:
            fecha = date.today().strftime("%d/%m/%Y")
            es_hoy = 'de hoy '
        if len(gasto) < 1:
            flash('Introduzca un id de gasto válido.', category='error')
        elif len(cuenta) < 1:
            flash('Introduzca un id de cuenta válido.', category='error')
        else:
            # Agregarlo a la base de datos
            try:
                n_pago = Pagos(fecha=fecha, id_gasto=gasto, cuenta=cuenta, monto_pagado=monto)
                db.session.add(n_pago)
                db.session.commit()
            except InternalError as e:
                flash(str(e.orig).split('CONTEXT')[0])
                db.session.rollback()
                return render_template('nuevo_pago.html', user=current_user)

            flash(f'El pago fue guardado con fecha {es_hoy}{fecha}.', category='success')
            return redirect(url_for('views.pagos'))



    return render_template('nuevo_pago.html', user=current_user)

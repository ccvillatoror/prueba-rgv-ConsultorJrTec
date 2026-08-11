from datetime import date
from db import db 
from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from models.cuentas import Cuentas
from models.gastos import Gastos
from models.pagos import Pagos
from sqlalchemy import update, text
from sqlalchemy.exc import InternalError, IntegrityError

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
    todos_gastos = db.session.execute(
        db.select(Gastos).order_by(Gastos.id)
        ).scalars().all()
    return render_template('ver_gastos.html', user=current_user, gastos=todos_gastos)

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
                flash(str(e.orig).split('CONTEXT')[0], category='error')
                db.session.rollback()
                return render_template('nuevo_gasto.html', user=current_user)
            except IntegrityError as e:
                db.session.rollback()
                flash(f'Ha sucedido un error inesperado. Intente más tarde. \nCódigo: {e.orig.pgcode}', category='error')
                return render_template('nuevo_gasto.html', user=current_user)


            flash(f'El gasto fue guardado con fecha {es_hoy}{fecha}.', category='success')
            return redirect(url_for('views.gastos'))

        
            
    return render_template('nuevo_gasto.html', user=current_user)


@view_bp.route('/aprobar-gasto', methods=['POST'])
@login_required
def aprobar_gasto():
    data = request.get_json()
    gasto_id = data.get('gasto_id')

    gasto_bd = db.session.get(Gastos, gasto_id)

    if not gasto_bd:
        flash('Artículo no econtroado', category='error')
        return jsonify({'error': 'Artículo no encontrado'}), 404
    try: 
        db.session.execute(
            update(Gastos)
            .where(Gastos.id == gasto_id)
            .values(estado='Aprobado')
            )

        db.session.commit()

    except InternalError as e:
        descripción_error = str(e.orig).split('CONTEXT')[0]
        flash(descripción_error, category='error')
        db.session.rollback()
        return jsonify({'error': descripción_error}), 404

    return jsonify({'success': True})


@view_bp.route('/pagar-gasto/<int:gasto_id>', methods=['GET'])
@login_required
def pagar_gasto(gasto_id):
    gasto_bd = db.session.get(Gastos, gasto_id)

    if not gasto_bd:
        flash('Artículo no encontrado', category='error')
        return redirect(url_for('views.gastos'))

    return redirect(url_for('views.nuevo_pago', gasto_id=gasto_id))


@view_bp.route('/cancelar-gasto', methods=['POST'])
@login_required
def cancelar_gasto():
    data = request.get_json(force=True)
    gasto_id = data.get('gasto_id')

    gasto_bd = db.session.get(Gastos, gasto_id)

    if not gasto_bd:
        flash('Artículo no encontrado', category='error')
        return jsonify({'error': 'Artículo no encontrado'}), 404
    try:
        db.session.execute(
            update(Gastos)
            .where(Gastos.id == gasto_id)
            .values(estado='Cancelado')
            )

        db.session.commit()

    except InternalError as e:
        descripción_error = str(e.orig).split('CONTEXT')[0]
        flash(descripción_error, category='error')
        db.session.rollback()
        return jsonify({'error': descripción_error}), 404

    return jsonify({'success': True})


@view_bp.route('/pagos/')
@view_bp.route('/pagos')
@login_required
def pagos():
    todos_pagos = db.session.execute(
        db.select(Pagos).order_by(Pagos.id)
    ).scalars().all()
    return render_template('ver_pagos.html', user=current_user, pagos=todos_pagos)

@view_bp.route('/pagos/nuevo/', methods=['GET', 'POST'])
@view_bp.route('/pagos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_pago():
    gastos_aprobados = db.session.execute(
        db.select(Gastos).where(Gastos.estado == 'Aprobado').order_by(Gastos.id)
        ).scalars().all()
    cuentas = db.session.execute(
        db.select(Cuentas).order_by(Cuentas.id)
        ).scalars().all()

    gasto_seleccionado = request.args.get('gasto_id', type=int)
    
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
                flash(str(e.orig).split('CONTEXT')[0], category='error')
                db.session.rollback()
                return render_template('nuevo_pago.html', user=current_user, gastos_aprobados=gastos_aprobados, cuentas=cuentas, gasto_seleccionado=gasto_seleccionado)
            except IntegrityError as e:
                db.session.rollback()
                flash(f'Ha sucedido un error inesperado. Intente más tarde. \nCódigo: {e.orig.pgcode}', category='error')
                return render_template('nuevo_pago.html', user=current_user, gastos_aprobados=gastos_aprobados, cuentas=cuentas, gasto_seleccionado=gasto_seleccionado)
            
            flash(f'El pago fue guardado con fecha {es_hoy}{fecha}.', category='success')
            flash('Para que el pago sea aplicado debe ser aprobado.', category='warning')
            return redirect(url_for('views.pagos'))



    return render_template('nuevo_pago.html', user=current_user, gastos_aprobados=gastos_aprobados, cuentas=cuentas, gasto_seleccionado=gasto_seleccionado)

@view_bp.route('/aprobar-pago', methods=['POST'])
@login_required
def aprobar_pago():
    data = request.get_json()
    pago_id = data.get('pago_id')

    pago_bd = db.session.get(Pagos, pago_id)

    if not pago_bd:
        flash('Artículo no econtroado', category='error')
        return jsonify({'error': 'Artículo no encontrado'}), 404
    try: 
        db.session.execute(
            update(Pagos)
            .where(Pagos.id == pago_id)
            .values(estado='Aprobado')
            )

        db.session.commit()

    except InternalError as e:
        descripción_error = str(e.orig).split('CONTEXT')[0]
        flash(descripción_error, category='error')
        db.session.rollback()
        return jsonify({'error': descripción_error}), 404

    return jsonify({'success': True})

@view_bp.route('/cancelar-pago', methods=['POST'])
@login_required
def cancelar_pago():
    data = request.get_json(force=True)
    pago_id = data.get('pago_id')

    pago_bd = db.session.get(Pagos, pago_id)

    if not pago_bd:
        flash('Artículo no encontrado', category='error')
        return jsonify({'error': 'Artículo no encontrado'}), 404
    try:
        db.session.execute(
            update(Pagos)
            .where(Pagos.id == pago_id)
            .values(estado='Cancelado')
            )

        db.session.commit()

    except InternalError as e:
        descripción_error = str(e.orig).split('CONTEXT')[0]
        flash(descripción_error, category='error')
        db.session.rollback()
        return jsonify({'error': descripción_error}), 404

    return jsonify({'success': True})

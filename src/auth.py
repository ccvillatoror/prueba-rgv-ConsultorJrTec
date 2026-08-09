from db import db

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from models.usuarios import Usuarios
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usr = request.form.get('user')
        pwd = request.form.get('password')

        usuario = Usuarios.query.filter_by(usuario=usr).first()
        if usuario:
            if check_password_hash(usuario.contraseña, pwd):
                flash('Ha ingresado correctamente', category='success')
                login_user(usuario, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Contraseña incorrecta, vuelva a intentarlo', category='error')
        else:
            flash('El usuario no existe', category='error')
            
    return render_template('login.html', user=current_user)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


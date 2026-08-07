from flask import Blueprint, render_template, request, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usr = request.form.get('user')
        pwd = request.form.get('password')

        if len(usr) < 3:
            flash('Introduzca un usario válido.', category='error')
        elif len(pwd) < 3:
            flash('Introduzca una contraseña válida.', category='error')
        else:
            flash('¡Bienvenido/a!', category='success')

            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    return "<p>Logout</o>"


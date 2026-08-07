from flask import Blueprint, render_template, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    return "<p>Logout</o>"


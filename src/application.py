import os
from api import api_bp
from auth import auth_bp
from db import db
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from models.cuentas import Cuentas
from models.gastos import Gastos
from models.usuarios import Usuarios
from models.pagos import Pagos
from views import view_bp


def create_app():

    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']
    app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
    
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(view_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Base de datos
    usr = os.getenv("PSQL_USR")
    pwd = os.getenv("PSQL_PWD")
    host = os. getenv("PSQL_HOST")
    port = os.getenv("PSQL_PORT")
    db_name = os.getenv("PSQL_DB")
    schema_name = os.getenv('PSQL_SCHEMA')

    postgres_url = f"postgresql://{usr}:{pwd}@{host}:{port}/{db_name}?options=-csearch_path%3D{schema_name}"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url

    db.init_app(app)

    # Login y JWT
    login_manager = LoginManager()
    jwt = JWTManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Necesitas iniciar sesión primero."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    app.config['LOGIN_DISABLED'] = False
    app.config['TESTING'] = False   
    
    @login_manager.user_loader
    def load_user(id):
        return db.session.get(Usuarios, int(id))
        
    return app

application = create_app()

if __name__=="__main__":
    application.run(debug=True, host='0.0.0.0', port=8000)
import os

from flask import Flask
from waitress import serve

from dotenv import load_dotenv
from db import db


load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']

    from views import view_bp
    from auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(view_bp, url_prefix='/')

    # Base de datos
    usr = os.getenv("PSQL_USR")
    pwd = os.getenv("PSQL_PWD")
    host = os. getenv("PSQL_HOST")
    port = os.getenv("PSQL_PORT")
    db_name = os.getenv("PSQL_DB")
    schema_name = os.getenv('PSQL_SCHEMA')

    postgres_url = f"postgresql://{usr}:{pwd}@{host}:{port}/{db_name}?options=-csearch_path%3D{schema_name}"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url
    app.config['SQLALCHEMY_ENGINES'] = {'default': postgres_url}

    db.init_app(app)

    return app

application = create_app()

if __name__=="__main__":
    serve(application, host='0.0.0.0', port=8000)
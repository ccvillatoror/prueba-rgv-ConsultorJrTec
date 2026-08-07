import os

from dotenv import load_dotenv
from flask import Flask, render_template
from waitress import serve

from auth import auth_bp
from views import view_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ['APP_SECRET_KEY']
    print(os.getenv('APP_SECRET_KEY'))

    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(view_bp, url_prefix='/')

    return app


application = create_app()

if __name__=="__main__":
    serve(application, host='0.0.0.0', port=8000)
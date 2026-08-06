from flask import Flask, render_template
from waitress import serve

application = Flask(__name__)

@application.route("/")
@application.route("/index")
def home():
    return render_template("index.html")

if __name__=="__main__":
    serve(application, host='0.0.0.0', port=8000)
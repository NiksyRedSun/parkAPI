from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from forms import LoginForm, RegisterForm, PostForm, GetCharForm, ItemsPostForm
from flask_migrate import Migrate
from sqlalchemy import URL
from config import DB_HOST, DB_PASS, DB_USER, DB_PORT, DB_NAME
from models_func import *


url_object = URL.create(
    "postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

SECRET_KEY = "#asgfkjdklsfgjserutdfg-09423"
SQLALCHEMY_DATABASE_URI = url_object


app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)


db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)





@app.route("/", methods=["POST", "GET"])
def index():
    form = PostForm()
    flash("Приветики!", "success")
    return render_template("index.html", form=form)



@app.route("/profile/<id>", methods=["POST", "GET"])
def profile(id):
    form = PostForm()
    return render_template("index.html", form=form)


@app.route("/test")
def test():
    print(postParkingSlot(3, num=3, letter="B"))
    return "1"



@app.errorhandler(404)
def pageNotFound(error):
    return render_template("error404.html"), 404





if __name__ == "__main__":
    app.run(debug=True)

#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0')
#

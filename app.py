from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from forms import NewResidentForm, NewCarForm, TakeParkingSlotForm, TakeApartmentForm
from flask_migrate import Migrate
from sqlalchemy import URL
from config import DB_HOST, DB_PASS, DB_USER, DB_PORT, DB_NAME
from models_func import *
from spec_models_func import *
from routers.resident_routers import resident_blueprint
from routers.apartment_routers import apartment_blueprint
from routers.car_routers import car_blueprint
from routers.parking_slots_routers import parking_blueprint


# Все ошибки обрабатываются в роутах, чтобы в случае чего пользователь мог получить сигнал, о том, что что-то пошло не так
# Здесь создается URL для соединения БД и Flask приложения

url_object = URL.create(
    "postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)


# Здесь этот URL указывается как константа для приложения
SECRET_KEY = "#asgfkjdklsfgjserutdfg-09423"
SQLALCHEMY_DATABASE_URI = url_object


app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)


# Здесь происходит регистрация блупринтов (наборов роутеров)
app.register_blueprint(resident_blueprint, url_prefix='/resident')
app.register_blueprint(apartment_blueprint, url_prefix='/apartment')
app.register_blueprint(car_blueprint, url_prefix='/car')
app.register_blueprint(parking_blueprint, url_prefix='/parking_slot')


db.init_app(app)

# Здесь подключается миграция на алембике
migrate = Migrate(app, db, render_as_batch=True)



# Роут для вывода всех жителей
@app.route("/", methods=["POST", "GET"])
def index():
    resident_list = getResident()
    resident_list.sort(key=lambda x: (x.last_name, x.first_name, x.patronymic))
    return render_template("index.html", resident_list=resident_list)


# Роут на ошибку 404
@app.errorhandler(404)
def pageNotFound(error):
    return render_template("error404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)


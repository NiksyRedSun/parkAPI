from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from forms import NewResidentForm, NewCarForm, TakeParkingSlotForm, TakeApartmentForm
from flask_migrate import Migrate
from sqlalchemy import URL
from config import DB_HOST, DB_PASS, DB_USER, DB_PORT, DB_NAME
from models_func import *
from spec_models_func import *
import random
from test import *


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


# Роуты для работы с жителями

@app.route("/", methods=["POST", "GET"])
def index():
    resident_list = getResident()
    resident_list.sort(key=lambda x: (x.last_name, x.first_name, x.patronymic))
    return render_template("index.html", resident_list=resident_list)


@app.route("/resident/<resident_id>", methods=["POST", "GET"])
def resident(resident_id):
    try:
        resident = getResidentWithJoin(resident_id)
        return render_template("resident.html", resident=resident, str=str, len=len)

    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")

    return redirect(url_for('index'))


@app.route("/resident/new", methods=["POST", "GET"])
def new_resident():
    form = NewResidentForm()

    try:
        if request.method == "POST":
            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():
                postResident(form.last_name.data, form.first_name.data,
                             form.patronymic.data, form.pas_series.data, form.pas_number.data)
                flash("Житель успешно добавлен", "success")
                return redirect(url_for('index'))

            else:
                flash("Данные заполнены неверно", "error")
    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")

    return render_template("new_resident.html", form=form)


@app.route("/resident/edit", methods=["POST", "GET"])
def edit_resident():

    resident_id = request.args.get('resident_id')

    try:

        if resident_id is None:
            raise WrongPathException

        resident = getResident(resident_id)
        form = NewResidentForm(obj=resident)

        if request.method == "POST":

            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():

                data = dataFromForm(form.data)
                putResident(resident_id, **data)
                flash("Информация о жителе изменена", "success")
                return redirect(url_for('resident', resident_id=resident_id))

            else:
                flash("Данные заполнены неверно", "error")

    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")

    return render_template("new_resident.html", form=form)



@app.route("/resident/delete")
def delete_resident():
    resident_id = request.args.get('resident_id')

    try:
        if resident_id is None:
            raise WrongPathException

        deleteResident(resident_id)
        flash("Житель успешно удален", "success")

    except NoResidentFoundException as e:
        flash(e.__str__(), "error")

    except WrongPathException as e:
        flash(e.__str__(), "error")

    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")

    return redirect(url_for('index'))


# Роуты для работы с квартирами

@app.route("/apartment/leave/")
def leave_apartment():
    resident_id = request.args.get('resident_id')
    apartment_id = request.args.get('apartment_id')

    try:
        if resident_id is None or apartment_id is None:
            raise WrongPathException

        leaveApartment(resident_id, apartment_id)

        flash("Пользователь успешно покинул квартиру", "success")
        return redirect(url_for('resident', resident_id=resident_id))

    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except NoApartmentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('resident', resident_id=resident_id))

    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except NoApartmentAtResident as e:
        flash(e.__str__(), "error")
        return redirect(url_for('resident', resident_id=resident_id))

    except Exception:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")
        return redirect(url_for('resident', resident_id=resident_id))


@app.route("/apartment/take/", methods=["POST", "GET"])
def take_apartment():

    resident_id = request.args.get('resident_id')
    apartments = getApartments(resident_id)
    form = TakeApartmentForm(apartments)

    try:
        if resident_id is None:
            raise WrongPathException

        # Для проверки того, существует ли житель с таким ид, если нет, то вылетит ошибка
        resident = getResident(resident_id)

        if request.method == "POST":
            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():
                takeApartments(resident_id, form.data)
                flash("Квартиры успешно заняты", "success")
                return redirect(url_for('resident', resident_id=resident_id))

    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except NoApartmentSelected as e:
        flash(e.__str__(), "error")

    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")

    return render_template("take_apartment.html", form=form, resident_id=resident_id)


# Роуты для работы с автомобилями

@app.route("/car/new", methods=["POST", "GET"])
def new_car():
    form = NewCarForm()
    resident_id = request.args.get('resident_id')

    try:
        if resident_id is None:
            raise WrongPathException

        # Для проверки того, существует ли житель с таким ид, если нет, то вылетит ошибка
        resident = getResident(resident_id)
        if request.method == "POST":
            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():
                postCar(resident_id, form.model.data, form.plate.data)
                flash("Автомобиль успешно добавлен", "success")
                return redirect(url_for('resident', resident_id=resident_id))

            else:
                flash("Данные заполнены неверно", "error")

    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений")

    return render_template("new_car.html", form=form, resident_id=resident_id)


@app.route("/car/edit", methods=["POST", "GET"])
def edit_car():


    resident_id = request.args.get('resident_id')
    car_id = request.args.get('car_id')

    try:
        if resident_id is None or car_id is None:
            raise WrongPathException

        # Для проверки того, существует ли житель с таким ид, если нет, то вылетит ошибка
        resident = getResident(resident_id)
        car = getCar(car_id)
        form = NewCarForm(obj=car)

        if request.method == "POST":
            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():
                data = dataFromForm(form.data)
                putCar(car_id, **data)
                flash("Информация об автомобиле изменена", "success")
                return redirect(url_for('resident', resident_id=resident_id))

            else:
                flash("Данные заполнены неверно", "error")

    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений")

    return render_template("new_car.html", form=form, resident_id=resident_id)



@app.route("/car/delete/")
def delete_car():
    resident_id = request.args.get('resident_id')
    car_id = request.args.get('car_id')

    try:
        if resident_id is None or car_id is None:
            raise WrongPathException

        deleteCar(car_id)
        flash("Автомобиль успешно удален", "success")
        return redirect(url_for('resident', resident_id=resident_id))

    except NoCarFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('resident', resident_id=resident_id))

    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except Exception:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")
        return redirect(url_for('resident', resident_id=resident_id))


# Роуты для работы с парковочными местами

@app.route("/parking_slot/leave/")
def leave_parking_slot():
    resident_id = request.args.get('resident_id')
    parking_slot_id = request.args.get('parking_slot_id')

    try:
        if resident_id is None or parking_slot_id is None:
            raise WrongPathException

        leaveSlot(resident_id, parking_slot_id)

        flash("Пользователь успешно покинул парковочное место", "success")
        return redirect(url_for('resident', resident_id=resident_id))

    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except NoParkingSlotFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('resident', resident_id=resident_id))

    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except NoParkingSlotAtResident as e:
        flash(e.__str__(), "error")
        return redirect(url_for('resident', resident_id=resident_id))

    except Exception:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")
        return redirect(url_for('resident', resident_id=resident_id))



@app.route("/parking_slot/take/", methods=["POST", "GET"])
def take_parking_slot():

    resident_id = request.args.get('resident_id')
    free_slots = getFreeSlots()
    form, slots_num = TakeParkingSlotForm(free_slots)

    try:
        if resident_id is None:
            raise WrongPathException

        # Для проверки того, существует ли житель с таким ид, если нет, то вылетит ошибка
        resident = getResident(resident_id)

        if request.method == "POST":
            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():
                takeFreeSlots(resident_id, form.data)

                flash("Парковочные места успешно заняты", "success")
                return redirect(url_for('resident', resident_id=resident_id))


    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except NoParkingSlotSelected as e:
        flash(e.__str__(), "error")

    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")

    return render_template("take_parking_slot.html", form=form, resident_id=resident_id, slots_num=slots_num)






# @app.route("/test")
# def test():
#     num_it = iter(list(range(1, 31)))
#     with db.session() as session:
#         for i in range(6, 35):
#             putApartment(i, num=next(num_it))
#
#     return generate_random_car_number()






@app.errorhandler(404)
def pageNotFound(error):
    return render_template("error404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)

#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0')
#

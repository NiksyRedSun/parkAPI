from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response, Blueprint
from forms import NewResidentForm, NewCarForm, TakeParkingSlotForm, TakeApartmentForm
from flask_migrate import Migrate
from sqlalchemy import URL
from config import DB_HOST, DB_PASS, DB_USER, DB_PORT, DB_NAME
from models_func import *
from spec_models_func import *


car_blueprint = Blueprint('car_blueprint', __name__)




# Роуты для работы с автомобилями

@car_blueprint.route("/new", methods=["POST", "GET"])
def new_car():
    # создание формы
    form = NewCarForm()

    # получение параметров из запроса
    resident_id = request.args.get('resident_id')

    try:
        if resident_id is None:
            raise WrongPathException

        # Для проверки того, существует ли житель с таким ид, если нет, то вылетит ошибка
        if request.method == "POST":

            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():
                # если все хорошо, до используем функцию для добавления данных
                postCar(resident_id, form.model.data, form.plate.data)
                flash("Автомобиль успешно добавлен", "success")
                return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

            else:
                flash("Данные заполнены неверно", "error")

    # исключения на случай возникающих ошибок
    # Если не найден данный житель
    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    # Если запрос передан без необходимых параметров
    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений")

    return render_template("new_car.html", form=form, resident_id=resident_id)


# роут на изменение автомобиля
@car_blueprint.route("/edit", methods=["POST", "GET"])
def edit_car():

    # получение параметров из запроса
    resident_id = request.args.get('resident_id')
    car_id = request.args.get('car_id')

    try:
        # проверка того, что они вообще были
        if resident_id is None or car_id is None:
            raise WrongPathException

        # Для проверки того, существует ли житель с таким ид, если нет, то вылетит ошибка
        resident = getResident(resident_id)

        # получение автомобиля и добавление информации о нем в форму
        car = getCar(car_id)
        form = NewCarForm(obj=car)

        if request.method == "POST":
            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():
                # вытаскиваем данные из формы с помощью созданной функции
                data = dataFromForm(form.data)
                # используем функцию для обновления данных
                putCar(car_id, **data)
                flash("Информация об автомобиле изменена", "success")
                return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

            else:
                flash("Данные заполнены неверно", "error")

    # блок обработки исключений
    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений")

    return render_template("new_car.html", form=form, resident_id=resident_id)


# роут для удаления автомобиля
@car_blueprint.route("/delete/")
def delete_car():
    # получение дополнительных параметров из запроса
    resident_id = request.args.get('resident_id')
    car_id = request.args.get('car_id')

    # проверка, были ли они
    try:
        if resident_id is None or car_id is None:
            raise WrongPathException

        # если все хорошо, то удаление автомобиля, перенаправление и вывод информации пользователю
        deleteCar(car_id)
        flash("Автомобиль успешно удален", "success")
        return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

    # блок обработки исключений
    except NoCarFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except Exception:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")
        return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

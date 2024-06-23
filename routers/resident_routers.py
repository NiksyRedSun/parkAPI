from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for
from forms import NewResidentForm
from models_func import *
from spec_models_func import *



resident_blueprint = Blueprint('resident_blueprint', __name__)

# Роуты для работы с жителями


# просто посмотреть на жителя
@resident_blueprint.route("/<resident_id>", methods=["POST", "GET"])
def resident(resident_id):
    try:
        # функция, которая подгружает с жителем всю информацию
        resident = getResidentWithJoin(resident_id)
        return render_template("resident.html", resident=resident, str=str, len=len)

    # исключения
    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")

    return redirect(url_for('index'))

# создание нового жителя
@resident_blueprint.route("/new", methods=["POST", "GET"])
def new_resident():
    # форма под это дело
    form = NewResidentForm()

    try:
        if request.method == "POST":
            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():
                # добавление нового жителя с помощью функции
                postResident(form.last_name.data, form.first_name.data,
                             form.patronymic.data, form.pas_series.data, form.pas_number.data)
                flash("Житель успешно добавлен", "success")
                return redirect(url_for('index'))

            else:
                flash("Данные заполнены неверно", "error")
    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")

    return render_template("new_resident.html", form=form)


@resident_blueprint.route("/edit", methods=["POST", "GET"])
def edit_resident():
    # получение параметров из запроса
    resident_id = request.args.get('resident_id')

    try:
        # проверка на то, были ли они вообще
        if resident_id is None:
            raise WrongPathException

        # получение жителя и добавление информации о нем в форму для удобного редактирования
        resident = getResident(resident_id)
        form = NewResidentForm(obj=resident)

        if request.method == "POST":

            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():

                # получение данных из формы и отправка в функцию изменения жителя
                data = dataFromForm(form.data)
                putResident(resident_id, **data)
                flash("Информация о жителе изменена", "success")
                return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

            else:
                flash("Данные заполнены неверно", "error")

    # блок исключений
    # на существование жителя с данным id
    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    # были ли вообще необходимые параметры в пути
    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    except:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")

    return render_template("new_resident.html", form=form)


# удаление жителя
@resident_blueprint.route("/delete")
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

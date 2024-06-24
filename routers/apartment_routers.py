from flask import render_template, request, flash, redirect, url_for, Blueprint
from forms import TakeApartmentForm
from models_func import *
from spec_models_func import *



apartment_blueprint = Blueprint('apartment_blueprint', __name__)



# Роуты для работы с квартирами

# Этот нужен для того чтобы была возможность покинуть квартиру
@apartment_blueprint.route("/apartment/leave")
def leave_apartment():

    # здесь подгружаются дополнительные параметры из запроса
    resident_id = request.args.get('resident_id')
    apartment_id = request.args.get('apartment_id')

    try:
        # Здесь происходит проверка на то, что эти параметры существуют, если нет, то при запросе пользователь
        # столкнется с ошибкой
        if resident_id is None or apartment_id is None:
            raise WrongPathException

        # непосредственно функция чтобы житель покинул квартиру
        leaveApartment(resident_id, apartment_id)

        # сообщение
        flash("Пользователь успешно покинул квартиру", "success")
        # перенаправление
        return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

    # блок обработки ошибок, на каждую возможную ошибку - обработчик

    # если житель с указанным id не найден
    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    # если квартира с указанным id не найдена
    except NoApartmentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

    # если нет дополнительных параметров в запросе
    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    # если вдруг данному жителю не принадлежит данная квартира по какой-то причине
    except NoApartmentAtResident as e:
        flash(e.__str__(), "error")
        return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

    # окончательный, просто чтобы пользователь знал, что что-то случилось и мог обратиться за помощью
    except Exception:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")
        return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))


@apartment_blueprint.route("/apartment/take/", methods=["POST", "GET"])
def take_apartment():

    # получение id из параметров запроса, получение апартаментов,
    resident_id = request.args.get('resident_id')


    try:
        if resident_id is None:
            raise WrongPathException

        # получение всех квартир
        apartments = getApartments(resident_id)
        # добавление всех квартир в форму
        form = TakeApartmentForm(apartments)

        # Для проверки того, существует ли житель с таким ид, если нет, то вылетит ошибка
        resident = getResident(resident_id)

        if request.method == "POST":
            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():
                takeApartments(resident_id, form.data)
                flash("Квартиры успешно заняты", "success")
                return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

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

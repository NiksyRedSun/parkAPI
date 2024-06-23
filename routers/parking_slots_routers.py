from flask import render_template, request, flash, redirect, url_for, Blueprint
from forms import TakeParkingSlotForm
from models_func import *
from spec_models_func import *


parking_blueprint = Blueprint('parking_blueprint', __name__)



# Роуты для работы с парковочными местами

# чтобы покинуть парковочное место
@parking_blueprint.route("/leave")
def leave_parking_slot():

    # получение дополнительных параметров
    resident_id = request.args.get('resident_id')
    parking_slot_id = request.args.get('parking_slot_id')

    try:
        # проверка на то были ли параметры
        if resident_id is None or parking_slot_id is None:
            raise WrongPathException

        # если были, то просто удаляем пользователя из места на парковке
        leaveSlot(resident_id, parking_slot_id)

        flash("Пользователь успешно покинул парковочное место", "success")
        return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

    # блоки исключений
    # если не найден пользователь
    except NoResidentFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    # если не найдено парковочное место
    except NoParkingSlotFoundException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

    # если не хватает параметров
    except WrongPathException as e:
        flash(e.__str__(), "error")
        return redirect(url_for('index'))

    # если вдруг по какой-то причине парковочный слот вообще не принадлежал пользователю
    except NoParkingSlotAtResident as e:
        flash(e.__str__(), "error")
        return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

    except Exception:
        flash("Что-то пошло не так, обратитесь к администратору для разъяснений", "error")
        return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))


# занимаем парковочное место
@parking_blueprint.route("/take", methods=["POST", "GET"])
def take_parking_slot():

    resident_id = request.args.get('resident_id')
    free_slots = getFreeSlots()
    # здесь функция возвращает два значения, в дальнейшем это будет использовано для изменения шаблона html
    form, slots_num = TakeParkingSlotForm(free_slots)

    try:
        # проверка параметров
        if resident_id is None:
            raise WrongPathException

        # Для проверки того, существует ли житель с таким ид, если нет, то вылетит ошибка
        resident = getResident(resident_id)

        if request.method == "POST":
            # проверка на то, отправленны ли какие-то данные в форму, а также проверка корректности данных
            if form.validate_on_submit():
                # если все хорошо, пользователь занимает слоты, которые отметил в форме
                takeFreeSlots(resident_id, form.data)

                flash("Парковочные места успешно заняты", "success")
                return redirect(url_for('resident_blueprint.resident', resident_id=resident_id))

    # блок обработки ошибок
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

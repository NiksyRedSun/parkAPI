from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Regexp


# в конце нужно будет добавить валидаторы:


class NewResidentForm(FlaskForm):
    last_name = StringField("Фамилия:", validators=[Length(min=2, max=30, message="Фамилия должна быть от 2 до 50 символов"),
                                                    Regexp("^[А-Яа-яЁё]+([-'][А-Яа-яЁё]+)*$",
                                                           message="Фамилия может состоять только из кирилических "
                                                                   "символов, включать в себя дефис и апострофы")])

    first_name = StringField("Имя:", validators=[Length(min=2, max=30, message="Имя должно быть от 2 до 50 символов"),
                                                 Regexp("^[А-Яа-яЁё]+([-'][А-Яа-яЁё]+)*$",
                                                        message="Имя может состоять только из кирилических "
                                                                "символов, включать в себя дефис и апострофы")])

    patronymic = StringField("Отчество:", validators=[Length(min=2, max=30, message=" Отчество должно быть от 2 до 50 символов"),
                                                      Regexp("^[А-Яа-яЁё]+([-'][А-Яа-яЁё]+)*$",
                                                             message="Отчество может состоять только из кирилических "
                                                                     "символов, включать в себя дефис и апострофы")
                                                      ])

    pas_series = StringField("Серия паспорта:", validators=[Regexp("^\d{2} \d{2}$",
                                                                   message="Серия паспорта указывается в формате 00 00")])

    pas_number = StringField("Номер паспорта:", validators=[Regexp("^\d{6}$",
                                                                   message="Номер паспорта указывается в формате 000000")])
    submit = SubmitField("Добавить")


class NewCarForm(FlaskForm):
    model = StringField("Модель:", validators=[Length(min=4, max=100, message="Модель быть от 4 до 100 символов")])
    plate = StringField("Номер:", validators=[Regexp("^[А-Я]\d{3}[А-Я]{2}$", message="Номер автомобиля указывается в формате А555АА")])
    submit = SubmitField("Добавить")


def TakeParkingSlotForm(free_slots):

    class TakeParkingSlotForm(FlaskForm):
        submit = SubmitField("Выбрать парковочные места")


    for slot in free_slots:
        setattr(TakeParkingSlotForm, f"id{slot.id}", BooleanField(f"Место {slot.letter + str(slot.num)}", default=False))


    form = TakeParkingSlotForm()
    return form, len(free_slots)


def TakeApartmentForm(apartments):

    class TakeApartmentForm(FlaskForm):
        submit = SubmitField("Выбрать квартиры")


    for apartment in apartments:
        setattr(TakeApartmentForm, f"id{apartment.id}", BooleanField(f"Квартира: {str(apartment.num)}. Жителей: {str(len(apartment.residents))}"
                                                                       , default=False))

    form = TakeApartmentForm()
    return form


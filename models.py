from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import Mapped, joinedload, subqueryload, lazyload
from sqlalchemy import desc
from typing import List

# создание бд
db = SQLAlchemy()

# команды чтобы были для быстрого доступа
# flask db migrate -m "message"
# flask db upgrade

# создание отдельной таблицы для связи многие ко многим в случае с жителями и квартирами
# (каждый житель может проживать в нескольких квартирах, в каждой квартире может проживать несколько жителей)
residence = db.Table('residence',
    db.Column('apartment_id', db.Integer, db.ForeignKey('apartments.id'), primary_key=True),
    db.Column('resident_id', db.Integer, db.ForeignKey('residents.id'), primary_key=True)
)

# валидация данных происходит в формах, перед отправкой
# модель для жителя
class Resident(db.Model):

    __tablename__ = 'residents'

    # должна быть уникальная комбинации серии и номера паспорта
    __table_args__ = (db.UniqueConstraint('pas_series', 'pas_number'),)

    # колонки
    id = db.Column(db.Integer, primary_key=True)

    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50), nullable=False)
    pas_series = db.Column(db.String(5), nullable=False)
    pas_number = db.Column(db.String(6), nullable=False)

    # связи для доступа к смежным сущностям (автомобилям, парковочным местам, квартирам)
    cars: Mapped[List["Car"]] = db.relationship(back_populates="resident", cascade="all,delete")
    parking_slots: Mapped[List["ParkingSlot"]] = db.relationship(back_populates="resident")
    apartments: Mapped[List["Apartment"]] = db.relationship("Apartment", secondary=residence, back_populates='residents',
                                                            lazy='subquery')

    def __repr__(self):
        return f"resident_id: {self.id}, resident_name: {self.first_name}"

# модель для квартир
class Apartment(db.Model):

    __tablename__ = 'apartments'
    # номер квартиры должен быть уникальным


    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=False, unique=True)

    # связи для доступа к смежным сущностям (жителям)
    residents: Mapped[List["Resident"]] = db.relationship("Resident", secondary=residence, back_populates="apartments",
                                                          lazy='subquery')

    def __repr__(self):
        return f"apartment_id: {self.id}, apartment_num: {self.num}"

# модель для автомобиля
class Car(db.Model):

    __tablename__ = 'cars'


    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.ForeignKey('residents.id', ondelete="CASCADE"), nullable=False)

    model = db.Column(db.String(20), nullable=False)
    # не должно быть полей с одинаковыми номерами
    plate = db.Column(db.String(6), nullable=False, unique=True)

    # связи для доступа к смежным сущностям (жителям)
    resident: Mapped["Resident"] = db.relationship(back_populates="cars")

    def __repr__(self):
        return f"car_id: {self.id}, car_plate {self.plate}"

# модель для парковочных слотов
class ParkingSlot(db.Model):

    __tablename__ = 'parking_slots'
    # комбинация цифры и буквы - уникальная
    __table_args__ = (db.UniqueConstraint('num', 'letter'), )

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.ForeignKey('residents.id', ondelete="CASCADE"), nullable=True)

    num = db.Column(db.Integer, nullable=False)
    letter = db.Column(db.String(1), nullable=False)

    # связи для доступа к смежным сущностям (жителям)
    resident: Mapped["Resident"] = db.relationship(back_populates="parking_slots")

    def __repr__(self):
        return f"parking_slot_id: {self.id}, number: {str(self.num) + self.letter}"


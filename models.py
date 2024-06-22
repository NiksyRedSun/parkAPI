from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import Mapped
from typing import List


db = SQLAlchemy()


class Resident(db.Model):

    __tablename__ = 'residents'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    pas_series = db.Column(db.Integer, nullable=False)
    pas_number = db.Column(db.Integer, nullable=False)

    cars: Mapped[List["Car"]] = db.relationship(back_populates="resident")
    parking_slots: Mapped[List["ParkingSlot"]] = db.relationship(back_populates="resident")
    apartments: Mapped[List["Apartment"]] = db.relationship(back_populates="resident")

    def __repr__(self):
        return f"resident_id: {self.id}, resident_name: {self.name}"


class Apartment(db.Model):

    __tablename__ = 'apartments'

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.ForeignKey('residents.id', ondelete="CASCADE"), nullable=False)

    num = db.Column(db.Integer, nullable=False)

    resident: Mapped["Resident"] = db.relationship(back_populates="apartments")


    def __repr__(self):
        return f"apartment_id: {self.id}"


class Car(db.Model):

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.ForeignKey('residents.id', ondelete="CASCADE"), nullable=False)

    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    plate = db.Column(db.String(50), nullable=False)

    resident: Mapped["Resident"] = db.relationship(back_populates="cars")

    def __repr__(self):
        return f"car_id: {self.id}"


class ParkingSlot(db.Model):

    __tablename__ = 'parking_slots'

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.ForeignKey('residents.id', ondelete="CASCADE"), nullable=False)

    num = db.Column(db.Integer, nullable=False)
    letter = db.Column(db.String(1), nullable=False)

    resident: Mapped["Resident"] = db.relationship(back_populates="parking_slots")

    def __repr__(self):
        return f"parking_slot: {self.id}"



def getResident(resident_id):
    with db.session() as s:
        try:
            res = Resident.query.get(resident_id)
            return res
        except:
            print("Что-то пошло не так при загрузке жителя")
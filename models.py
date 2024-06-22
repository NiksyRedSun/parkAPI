from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import Mapped
from typing import List


db = SQLAlchemy()

# flask db migrate -m "message"
# flask db upgrade


class Resident(db.Model):

    __tablename__ = 'residents'

    id = db.Column(db.Integer, primary_key=True)

    second_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    pas_series = db.Column(db.String(5), nullable=False, unique=True)
    pas_number = db.Column(db.String(6), nullable=False, unique=True)

    cars: Mapped[List["Car"]] = db.relationship(back_populates="resident")
    parking_slots: Mapped[List["ParkingSlot"]] = db.relationship(back_populates="resident")
    apartments: Mapped[List["Apartment"]] = db.relationship(back_populates="resident")

    def __repr__(self):
        return f"resident_id: {self.id}, resident_name: {self.first_name}"


class Apartment(db.Model):

    __tablename__ = 'apartments'
    __table_args__ = (db.UniqueConstraint('resident_id', 'num'),)

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.ForeignKey('residents.id', ondelete="CASCADE"), nullable=False)

    num = db.Column(db.Integer, nullable=False)

    resident: Mapped["Resident"] = db.relationship(back_populates="apartments")


    def __repr__(self):
        return f"apartment_id: {self.id}"


class Car(db.Model):

    __tablename__ = 'cars'
    __table_args__ = (db.UniqueConstraint('resident_id', 'plate'),)

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.ForeignKey('residents.id', ondelete="CASCADE"), nullable=False)

    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    plate = db.Column(db.String(50), nullable=False, unique=True)

    resident: Mapped["Resident"] = db.relationship(back_populates="cars")

    def __repr__(self):
        return f"car_id: {self.id}"


class ParkingSlot(db.Model):

    __tablename__ = 'parking_slots'
    __table_args__ = (db.UniqueConstraint('resident_id', 'num', 'letter'),)

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.ForeignKey('residents.id', ondelete="CASCADE"), nullable=False)

    num = db.Column(db.Integer, nullable=False)
    letter = db.Column(db.String(1), nullable=False)

    resident: Mapped["Resident"] = db.relationship(back_populates="parking_slots")

    def __repr__(self):
        return f"parking_slot: {self.id}"


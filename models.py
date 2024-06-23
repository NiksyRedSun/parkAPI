from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import Mapped, joinedload, subqueryload, lazyload
from sqlalchemy import desc
from typing import List


db = SQLAlchemy()

# flask db migrate -m "message"
# flask db upgrade


residence = db.Table('residence',
    db.Column('apartment_id', db.Integer, db.ForeignKey('apartments.id'), primary_key=True),
    db.Column('resident_id', db.Integer, db.ForeignKey('residents.id'), primary_key=True)
)

class Resident(db.Model):

    __tablename__ = 'residents'
    __table_args__ = (db.UniqueConstraint('pas_series', 'pas_number'),)

    id = db.Column(db.Integer, primary_key=True)

    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50), nullable=False)
    pas_series = db.Column(db.String(5), nullable=False)
    pas_number = db.Column(db.String(6), nullable=False)

    cars: Mapped[List["Car"]] = db.relationship(back_populates="resident", cascade="all,delete")
    parking_slots: Mapped[List["ParkingSlot"]] = db.relationship(back_populates="resident")
    apartments: Mapped[List["Apartment"]] = db.relationship("Apartment", secondary=residence, back_populates='residents',
                                                            lazy='subquery')

    def __repr__(self):
        return f"resident_id: {self.id}, resident_name: {self.first_name}"


class Apartment(db.Model):

    __tablename__ = 'apartments'
    __table_args__ = (db.UniqueConstraint('num'),)

    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=False)

    residents: Mapped[List["Resident"]] = db.relationship("Resident", secondary=residence, back_populates="apartments",
                                                          lazy='subquery')

    def __repr__(self):
        return f"apartment_id: {self.id}, apartment_num: {self.num}"


class Car(db.Model):

    __tablename__ = 'cars'
    __table_args__ = (db.UniqueConstraint('resident_id', 'plate'),)

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.ForeignKey('residents.id', ondelete="CASCADE"), nullable=False)

    model = db.Column(db.String(20), nullable=False)
    plate = db.Column(db.String(6), nullable=False, unique=True)

    resident: Mapped["Resident"] = db.relationship(back_populates="cars")

    def __repr__(self):
        return f"car_id: {self.id}, car_plate {self.plate}"


class ParkingSlot(db.Model):

    __tablename__ = 'parking_slots'
    __table_args__ = (db.UniqueConstraint('num', 'letter'), )

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.ForeignKey('residents.id', ondelete="CASCADE"), nullable=True)

    num = db.Column(db.Integer, nullable=False)
    letter = db.Column(db.String(1), nullable=False)

    resident: Mapped["Resident"] = db.relationship(back_populates="parking_slots")

    def __repr__(self):
        return f"parking_slot_id: {self.id}, number: {str(self.num) + self.letter}"


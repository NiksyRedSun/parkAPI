from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Resident(db.Model):
    __tablename__ = 'residents'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    pas_series = db.Column(db.Integer)
    pas_number = db.Column(db.Integer)

    def __repr__(self):
        return f"resident_id: {self.id}, resident_name: {self.name}"


class Apartment(db.Model):
    __tablename__ = 'apartments'

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer)
    num = db.Column(db.Integer)


    def __repr__(self):
        return f"apartment_id: {self.id}"



def getResident(resident_id):
    with db.session() as s:
        try:
            res = Resident.query.get(resident_id)
            return res
        except:
            print("Что-то пошло не так при загрузке жителя")
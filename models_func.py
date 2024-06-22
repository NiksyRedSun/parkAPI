from models import *


class NoResidentFound(Exception):
    def __str__(self):
        return "Житель с запрашиваемым id не найден"

class NoApartmentFound(Exception):
    def __str__(self):
        return "Квартира с запрашиваемым id не найдена"

class NoCarFound(Exception):
    def __str__(self):
        return "Автомобиль с запрашиваемым id не найден"

class NoParkingSlotFound(Exception):
    def __str__(self):
        return "Парковочное место с запрашиваемым id не найдено"

class NoObjectFound(Exception):
    def __str__(self):
        return "Объект с запрашиваемым id не найден"


# функции для работы с жителями

def getResident(resident_id=None):
    with db.session() as session:
        try:
            if resident_id is not None:
                res = Resident.query.get(resident_id)

                if res is None:
                    raise NoResidentFound()

                return res
            else:
                res = Resident.query.all()
                return res

        except Exception as e:
            print(e)


def postResident(last_name, first_name, patronymic, pas_series, pas_number):
    with db.session() as session:
        try:
            res = Resident(last_name=last_name, first_name=first_name, patronymic=patronymic,
                           pas_series=pas_series, pas_number=pas_number)
            session.add(res)
            session.commit()

        except Exception as e:
            print(e)


def putResident(resident_id, **kwargs):
    with db.session() as session:
        try:
            if kwargs:
                res = Resident.query.get(resident_id)

                if res is None:
                    raise NoResidentFound

                for key in kwargs:
                    setattr(res, key, kwargs[key])
                session.add(res)
                session.commit()

        except Exception as e:
            print(e)


def deleteResident(resident_id):
    with db.session() as session:
        try:
            res = Resident.query.get(resident_id)

            if res is None:
                raise NoResidentFound

            session.delete(res)
            session.commit()

        except Exception as e:
            print(e)


# функции для работы с апартаментами

def getApartment(apartment_id=None):
    with db.session() as session:
        try:
            if apartment_id is not None:
                res = Apartment.query.get(apartment_id)

                if res is None:
                    raise NoApartmentFound

                return res
            else:
                res = Apartment.query.all()
                return res

        except Exception as e:
            print(e)


def postApartment():
    with db.session() as session:
        try:
            res = Apartment()
            session.add(res)
            session.commit()

        except Exception as e:
            print(e)


def putApartment(apartment_id, **kwargs):
    with db.session() as session:
        try:
            if kwargs:
                res = Apartment.query.get(apartment_id)

                if res is None:
                    raise NoApartmentFound

                for key in kwargs:
                    setattr(res, key, kwargs[key])
                session.add(res)
                session.commit()

        except Exception as e:
            print(e)


def deleteApartment(apartment_id):
    with db.session() as session:
        try:
            res = Apartment.query.get(apartment_id)

            if res is None:
                raise NoApartmentFound

            session.delete(res)
            session.commit()

        except Exception as e:
            print(e)

# функции для работы с автомобилями

def getCar(car_id=None):
    with db.session() as session:
        try:
            if car_id is not None:
                res = Car.query.get(car_id)

                if res is None:
                    raise NoCarFound

                return res
            else:
                res = Car.query.all()
                return res

        except Exception as e:
            print(e)


def postCar(resident_id, model, plate):
    with db.session() as session:
        try:
            res = Car(resident_id=resident_id, model=model, plate=plate)
            session.add(res)
            session.commit()

        except Exception as e:
            print(e)


def putCar(car_id, **kwargs):
    with db.session() as session:
        try:
            if kwargs:
                res = Car.query.get(car_id)

                if res is None:
                    raise NoCarFound

                for key in kwargs:
                    setattr(res, key, kwargs[key])
                session.add(res)
                session.commit()

        except Exception as e:
            print(e)


def deleteCar(car_id):
    with db.session() as session:
        try:
            res = Car.query.get(car_id)

            if res is None:
                raise NoCarFound

            session.delete(res)
            session.commit()

        except Exception as e:
            print(e)


# функции для работы с парковочными местами

def getParkingSlot(slot_id=None):
    with db.session() as session:
        try:
            if slot_id is not None:
                res = ParkingSlot.query.get(slot_id)

                if res is None:
                    raise NoParkingSlotFound

                return res
            else:
                res = ParkingSlot.query.all()
                return res

        except Exception as e:
            print(e)


def postParkingSlot(num, letter):
    with db.session() as session:
        try:
            res = ParkingSlot(num=num, letter=letter)
            session.add(res)
            session.commit()

        except Exception as e:
            print(e)


def putParkingSlot(slot_id, **kwargs):
    with db.session() as session:
        try:
            if kwargs:
                res = ParkingSlot.query.get(slot_id)

                if res is None:
                    raise NoParkingSlotFound

                for key in kwargs:
                    setattr(res, key, kwargs[key])
                session.add(res)
                session.commit()

        except Exception as e:
            print(e)


def deleteParkingSlot(slot_id):
    with db.session() as session:
        try:
            res = ParkingSlot.query.get(slot_id)

            if res is None:
                raise NoParkingSlotFound

            session.delete(res)
            session.commit()

        except Exception as e:
            print(e)

# функции для работы с объектами в принципе

def getObject(Model, object_id=None):
    with db.session() as session:
        try:
            if object_id is not None:
                res = Model.query.get(object_id)

                if res is None:
                    raise NoObjectFound

                return res
            else:
                res = Model.query.all()
                return res

        except Exception as e:
            print(e)


def postObject(Model, **kwargs):
    with db.session() as session:
        try:
            res = Model(**kwargs)
            session.add(res)
            session.commit()

        except Exception as e:
            print(e)


def putObject(Model, object_id, **kwargs):
    with db.session() as session:
        try:
            if kwargs:
                res = Model.query.get(object_id)

                if res is None:
                    raise NoObjectFound

                for key in kwargs:
                    setattr(res, key, kwargs[key])
                session.add(res)
                session.commit()

        except Exception as e:
            print(e)


def deleteObject(Model, object_id):
    with db.session() as session:
        try:
            res = Model.query.get(object_id)

            if res is None:
                raise NoObjectFound

            session.delete(res)
            session.commit()

        except Exception as e:
            print(e)
from models import *

# Здесь расположены обычные функции и исключения под ORM


class NoResidentFoundException(Exception):
    def __str__(self):
        return "Житель с запрашиваемым id не найден"

class NoApartmentFoundException(Exception):
    def __str__(self):
        return "Квартира с запрашиваемым id не найдена"

class NoCarFoundException(Exception):
    def __str__(self):
        return "Автомобиль с запрашиваемым id не найден"

class NoParkingSlotFoundException(Exception):
    def __str__(self):
        return "Парковочное место с запрашиваемым id не найдено"

class NoObjectFoundException(Exception):
    def __str__(self):
        return "Объект с запрашиваемым id не найден"

class WrongPathException(Exception):
    def __str__(self):
        return "Неправильно указаны параметры запроса"


# функции для работы с жителями

# тестово убран блок try/except
def getResident(resident_id=None):
    with db.session() as session:

        if resident_id is not None:
            result = Resident.query.get(resident_id)

            if result is None:
                raise NoResidentFoundException

            return result
        else:
            result = Resident.query.all()
            return result



def postResident(last_name, first_name, patronymic, pas_series, pas_number):
    with db.session() as session:

        result = Resident(last_name=last_name, first_name=first_name, patronymic=patronymic,
                          pas_series=pas_series, pas_number=pas_number)
        session.add(result)
        session.commit()
        return result


def putResident(resident_id, **kwargs):
    with db.session() as session:
        try:
            if kwargs:
                result = Resident.query.get(resident_id)

                if result is None:
                    raise NoResidentFoundException

                for key in kwargs:
                    setattr(result, key, kwargs[key])
                session.add(result)
                session.commit()

        except Exception as e:
            print(e)


def deleteResident(resident_id):
    with db.session() as session:

        result = Resident.query.get(resident_id)

        if result is None:
            raise NoResidentFoundException

        session.delete(result)
        session.commit()


# функции для работы с апартаментами

def getApartment(apartment_id=None):
    with db.session() as session:
        try:
            if apartment_id is not None:
                result = Apartment.query.get(apartment_id)

                if result is None:
                    raise NoApartmentFoundException

                return result
            else:
                result = Apartment.query.all()
                return result

        except Exception as e:
            print(e)


def postApartment():
    with db.session() as session:
        try:
            result = Apartment()
            session.add(result)
            session.commit()
            return result

        except Exception as e:
            print(e)


def putApartment(apartment_id, **kwargs):
    with db.session() as session:
        try:
            if kwargs:
                result = Apartment.query.get(apartment_id)

                if result is None:
                    raise NoApartmentFoundException

                for key in kwargs:
                    setattr(result, key, kwargs[key])
                session.add(result)
                session.commit()

        except Exception as e:
            print(e)


def deleteApartment(apartment_id):
    with db.session() as session:
        try:
            result = Apartment.query.get(apartment_id)

            if result is None:
                raise NoApartmentFoundException

            session.delete(result)
            session.commit()

        except Exception as e:
            print(e)

# функции для работы с автомобилями

def getCar(car_id=None):
    with db.session() as session:
        try:
            if car_id is not None:
                result = Car.query.get(car_id)

                if result is None:
                    raise NoCarFoundException

                return result
            else:
                result = Car.query.all()
                return result

        except Exception as e:
            print(e)


def postCar(resident_id, model, plate):
    with db.session() as session:
        try:
            result = Car(resident_id=resident_id, model=model, plate=plate)
            session.add(result)
            session.commit()
            return result

        except Exception as e:
            print(e)


def putCar(car_id, **kwargs):
    with db.session() as session:
        try:
            if kwargs:
                result = Car.query.get(car_id)

                if result is None:
                    raise NoCarFoundException

                for key in kwargs:
                    setattr(result, key, kwargs[key])
                session.add(result)
                session.commit()

        except Exception as e:
            print(e)


def deleteCar(car_id):
    with db.session() as session:

        result = Car.query.get(car_id)

        if result is None:
            raise NoCarFoundException

        session.delete(result)
        session.commit()



# функции для работы с парковочными местами

def getParkingSlot(slot_id=None):
    with db.session() as session:
            if slot_id is not None:
                result = ParkingSlot.query.get(slot_id)

                if result is None:
                    raise NoParkingSlotFoundException

                return result
            else:
                result = ParkingSlot.query.all()
                return result



def postParkingSlot(num, letter):
    with db.session() as session:
        try:
            result = ParkingSlot(num=num, letter=letter)
            session.add(result)
            session.commit()
            return result

        except Exception as e:
            print(e)


def putParkingSlot(slot_id, **kwargs):
    with db.session() as session:
        try:
            if kwargs:
                result = ParkingSlot.query.get(slot_id)

                if result is None:
                    raise NoParkingSlotFoundException

                for key in kwargs:
                    setattr(result, key, kwargs[key])
                session.add(result)
                session.commit()

        except Exception as e:
            print(e)


def deleteParkingSlot(slot_id):
    with db.session() as session:
        try:
            result = ParkingSlot.query.get(slot_id)

            if result is None:
                raise NoParkingSlotFoundException

            session.delete(result)
            session.commit()

        except Exception as e:
            print(e)

# функции для работы с объектами в принципе

def getObject(Model, object_id=None):
    with db.session() as session:
        try:
            if object_id is not None:
                result = Model.query.get(object_id)

                if result is None:
                    raise NoObjectFoundException

                return result
            else:
                result = Model.query.all()
                return result

        except Exception as e:
            print(e)


def postObject(Model, **kwargs):
    with db.session() as session:
        try:
            result = Model(**kwargs)
            session.add(result)
            session.commit()
            return result

        except Exception as e:
            print(e)


def putObject(Model, object_id, **kwargs):
    with db.session() as session:
        try:
            if kwargs:
                result = Model.query.get(object_id)

                if result is None:
                    raise NoObjectFoundException

                for key in kwargs:
                    setattr(result, key, kwargs[key])
                session.add(result)
                session.commit()

        except Exception as e:
            print(e)


def deleteObject(Model, object_id):
    with db.session() as session:
        try:
            result = Model.query.get(object_id)

            if result is None:
                raise NoObjectFoundException

            session.delete(result)
            session.commit()

        except Exception as e:
            print(e)
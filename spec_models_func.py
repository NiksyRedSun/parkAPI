from models import *
from models_func import NoResidentFoundException, NoObjectFoundException, \
    NoApartmentFoundException, NoCarFoundException, NoParkingSlotFoundException

# Здесь расположены специальные функции для определенных операций

class NoParkingSlotAtResident(Exception):
    def __str__(self):
        return "Жителю не принадлежит это парковочное место"

class NoApartmentAtResident(Exception):
    def __str__(self):
        return "Жителю не принадлежит эта квартира"

class NoParkingSlotSelected(Exception):
    def __str__(self):
        return "Не выбрано ни одного парковочного места"


# функции для жителей
def getResidentWithJoin(resident_id):
    with db.session() as session:

        resident = Resident.query.options(joinedload(Resident.cars),
                                        joinedload(Resident.apartments),
                                        joinedload(Resident.parking_slots)).get(resident_id)
        if resident is None:
            raise NoResidentFoundException

        for apartment in resident.apartments:
            print(apartment.residents)

        return resident


# функции для парковочных мест
def leave_slot(resident_id, parking_slot_id):
    with db.session() as session:

        resident = Resident.query.options(joinedload(Resident.parking_slots)).get(resident_id)
        parking_slot = ParkingSlot.query.get(parking_slot_id)

        if parking_slot is None:
            raise NoParkingSlotFoundException

        if resident is None:
            raise NoResidentFoundException

        if parking_slot in resident.parking_slots:
            resident.parking_slots.remove(parking_slot)
            session.add(resident)
            session.commit()
        else:
            raise NoParkingSlotAtResident

def get_free_slots():
    with db.session() as session:

        slots = ParkingSlot.query.filter(ParkingSlot.resident_id==None).all()
        slots.sort(key=lambda x: (x.letter, x.num))
        return slots


def take_free_slots(resident_id, data):
    with db.session() as session:

        resident = Resident.query.get(resident_id)

        if resident is None:
            raise NoResidentFoundException

        del data['submit']
        del data['csrf_token']

        slots_ids = list(filter(lambda x: data[x], data))
        if slots_ids:
            slots_ids = list(map(lambda x: int(x[2:]), slots_ids))
            for id in slots_ids:
                slot = ParkingSlot.query.get(id)
                slot.resident = resident
                session.add(slot)
                session.commit()

        else:
            raise NoParkingSlotSelected



# функции для квартир
def leave_apartment_func(resident_id, apartment_id):
    with db.session() as session:

        resident = Resident.query.options(joinedload(Resident.apartments)).get(resident_id)
        apartment = Apartment.query.get(apartment_id)

        if apartment is None:
            raise NoApartmentFoundException

        if resident is None:
            raise NoResidentFoundException

        if apartment in resident.apartments:
            resident.apartments.remove(apartment)
            session.add(resident)
            session.commit()
        else:
            raise NoApartmentAtResident




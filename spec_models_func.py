from models import *
from models_func import NoResidentFoundException, NoObjectFoundException, \
    NoApartmentFoundException, NoCarFoundException, NoParkingSlotFoundException

# Здесь расположены специальные функции для определенных операций


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

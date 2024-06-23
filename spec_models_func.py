from models import *
from models_func import NoResidentFoundException, NoObjectFoundException, \
    NoApartmentFoundException, NoCarFoundException, NoParkingSlotFoundException


# специальные исключения для неклассических ситуаций
class NoParkingSlotAtResident(Exception):
    def __str__(self):
        return "Жителю не принадлежит это парковочное место"

class NoApartmentAtResident(Exception):
    def __str__(self):
        return "Жителю не принадлежит эта квартира"

class NoParkingSlotSelected(Exception):
    def __str__(self):
        return "Не выбрано ни одного парковочного места"

class NoApartmentSelected(Exception):
    def __str__(self):
        return "Не выбрана ни одна квартира"



# Здесь расположены специальные функции для определенных операций
# функции для жителей


def getResidentWithJoin(resident_id):
    with db.session() as session:

        # получаем жителя, вместе со всеми атрибутами
        resident = Resident.query.options(joinedload(Resident.cars),
                                        joinedload(Resident.apartments),
                                        joinedload(Resident.parking_slots)).get(resident_id)

        # проверяем существует ли он в принципе
        if resident is None:
            raise NoResidentFoundException

        for apartment in resident.apartments:
            apartment.residents

        session.add(resident)

        return resident


# функции для парковочных мест
# функция для того чтобы "сдать" парковочное место
def leaveSlot(resident_id, parking_slot_id):
    with db.session() as session:
        # загружаем жителя и место для парковки
        resident = Resident.query.options(joinedload(Resident.parking_slots)).get(resident_id)
        parking_slot = ParkingSlot.query.get(parking_slot_id)

        # проверяем существуют ли они вообще
        if parking_slot is None:
            raise NoParkingSlotFoundException

        if resident is None:
            raise NoResidentFoundException

        # если существуют и данному жителю принадлежит данное парковочное место, то удаляем его из него и коммитим
        if parking_slot in resident.parking_slots:
            resident.parking_slots.remove(parking_slot)
            session.add(resident)
            session.commit()
        # если не принадлежит, то поднимаем ошибку
        else:
            raise NoParkingSlotAtResident

# функция для того, чтобы получить пустые парковочные места
def getFreeSlots():
    with db.session() as session:

        # получаем не занятые парковочные места
        slots = ParkingSlot.query.filter(ParkingSlot.resident_id==None).all()
        # сортировка по буквам и цифрам
        slots.sort(key=lambda x: (x.letter, x.num))
        return slots

# функция для того чтобы получить все квартиры
def getApartments(resident_id):
    with db.session() as session:
        # получаем жителя
        resident = Resident.query.get(resident_id)
        # получаем все квартиры
        apartments = Apartment.query.options(joinedload(Apartment.residents)).all()
        # оставляем только те, в которых нет нашего жителя
        apartments = list(filter(lambda x: resident not in x.residents, apartments))
        # сортируем
        apartments.sort(key=lambda x: x.num)

        return apartments

# функция для того чтобы "занять" квартиру
# принимает в себя id пользователя и данные - словарь, привязанный к формам
def takeFreeSlots(resident_id, data: dict):
    with db.session() as session:

        # получаем жителя
        resident = Resident.query.get(resident_id)

        # проверяем существует ли он
        if resident is None:
            raise NoResidentFoundException

        # удаляем из подгруженных данных ненужные
        del data['submit']
        del data['csrf_token']

        # оставляем только те парковочные слоты, в которых стоит значение True, то есть они были выбраны жителем для того чтобы их занять
        slots_ids = list(filter(lambda x: data[x], data))
        # если они есть, то работаем, иначе - означает, что пользователь не выбрал ни одного парковочного слота
        if slots_ids:
            # оставляем только цифры из записи и преобразуем их в числа
            slots_ids = list(map(lambda x: int(x[2:]), slots_ids))

            # пробегаемся по каждому используя как id для получения сущности парковочного места
            for id in slots_ids:
                slot = ParkingSlot.query.get(id)
                # устанавливаем туда жителя как владельца
                slot.resident = resident
                session.add(slot)
                session.commit()

        else:
            raise NoParkingSlotSelected

# функция для того чтобы "занять" квартиру, получает в себя id пользователя и данные из формы
def takeApartments(resident_id, data: dict):
    with db.session() as session:

        # получаем жителя
        resident = Resident.query.get(resident_id)

        # проверяем был ли он
        if resident is None:
            raise NoResidentFoundException

        # удаляем лишнюю информацию из данных
        del data['submit']
        del data['csrf_token']

        # оставляем только idишники тех квартир, которые пользователь выбрал (имеют значение True по ключу)
        apartments_ids = list(filter(lambda x: data[x], data))

        # проверяем были ли такие, если нет - то исключение
        if apartments_ids:
            # если да, то преобразуем все в числа
            apartments_ids = list(map(lambda x: int(x[2:]), apartments_ids))

            # используем эти числа для того чтобы получить каждую квартиру и вселить туда нашего жителя
            for id in apartments_ids:
                apartment = Apartment.query.get(id)
                apartment.residents.append(resident)
                session.add(apartment)
                session.commit()

        else:
            raise NoApartmentSelected



# функция позволяет покинуть квартиру
def leaveApartment(resident_id, apartment_id):
    with db.session() as session:

        # получем апартаменты и пользователя
        resident = Resident.query.options(joinedload(Resident.apartments)).get(resident_id)
        apartment = Apartment.query.get(apartment_id)

        # проверяем на то, были ли они
        if apartment is None:
            raise NoApartmentFoundException

        if resident is None:
            raise NoResidentFoundException

        # если были, то проверяем "прописан" ли конкретный житель в конкретной квартире
        # если прописан, то удаляем его от туда, если нет, то поднимаем исключение
        if apartment in resident.apartments:
            resident.apartments.remove(apartment)
            session.add(resident)
            session.commit()
        else:
            raise NoApartmentAtResident

# функция для того чтобы удалить из данных формы ненужную информацию
def dataFromForm(data: dict):

    del data['submit']
    del data['csrf_token']

    return data
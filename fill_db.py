from app import *
import random



# конструкция конечно так себе, сделан на скорую руку

# @app.route("/test")
# def test_router():
#     with db.session() as session:
#         try:
#             for i in range(1, 101):
#                 if i in list(range(1, 21)):
#                     slot = postParkingSlot(i % 21, "A")
#                 if i in list(range(21, 41)):
#                     slot = postParkingSlot(i % 21, "B")
#                 if i in list(range(41, 61)):
#                     slot = postParkingSlot(i % 21, "C")
#                 if i in list(range(61, 81)):
#                     slot = postParkingSlot(i % 21, "D")
#                 if i in list(range(81, 101)):
#                     slot = postParkingSlot(i % 21, "E")
#                 session.add(slot)
#                 session.commit()
#
#             for i in range(1, 31):
#                 apartment = Apartment(num=i)
#                 session.add(apartment)
#                 session.commit()
#             return "База заполнена"
#         except:
#             print("что-то пошло не так")






import uvicorn
from fastapi import Request, Depends, FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from tablesnrouters.router import router as router
from starlette.staticfiles import StaticFiles


app = FastAPI(
    title="parkAPI"
)




@app.get("/")
async def index(request: Request):
    return "Tvoya mat'"


#
# @app.get("/second_test")
# # async def test_router(request: Request, session: AsyncSession = Depends(get_async_session)):
# async def test_router(request: Request, user: User | None = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
#     gameplay = gameplays[user.id]
#     messages = await gameplay.get_notifications(session)
#     await gameplay.get_count_unread_notifications(session)
#     print()


#
# @app.get("/test")
# # async def test_router(request: Request, session: AsyncSession = Depends(get_async_session)):
# async def test_router(request: Request):
#     # Получить сессию
#     session = async_session_maker()
#     async with session:
#         # Получить объект
#         # print(await session.get(User, 1))
#         # Можно делать запросы сразу с нескольких таблиц, в документации показано, как
#         query = select(TownSquare.cur_level).where(TownSquare.user_id == 1)
#         pre_result = await session.execute(query)
#
#         # print(type(pre_result))
#         # различные варианты работы с resultом (который в данном случае зовется pre_result)
#         # print(list(pre_result))
#         # print(pre_result.fetchall())
#         # print(pre_result.all())
#         # print(pre_result.one())
#         # Без scalars возвращает объекты в кортежах, если хочешь вытаскивать объекты из кортежей, используй scalars
#         # print(pre_result.scalars().one())
#         # строка ниже заменяет предыдущую
#         print(pre_result.scalar_one())
#
#         # Сешн коммит нужен только в том случае, если мы изменяли какие-либо данные внутри сессии
#         # session.commit()
#         # Можно использовать, чтобы удалять объекты
#         # session.delete()


# Ниже стандартный способ работы с sqlalchemy
#     query = select(User).where(User.username == user)
#     pre_result = await session.execute(query)
#     result = pre_result.fetchall()
# Через select и result


# # можно использовать такую конструкцию для работы в sqla
# with async_session_maker() as session:
#     session.begin()
#     try:
#         session.add(some_object)
#         session.add(some_other_object)
#     except:
#         session.rollback()
#         raise
#     else:
#         session.commit()

# Еще более "удобный" вариант, не требующий коммита в конце
# with async_session_maker() as session, session.begin():
#     session.add(some_object)
#     session.add(some_other_object)




# Ниже два роутера - для аутентификации и регистрации
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth/jwt",
#     tags=["auth"],
# )
#
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )


#
app.include_router(router)




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000)




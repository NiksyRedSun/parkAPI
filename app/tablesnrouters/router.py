from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from config import templates
from fastapi.responses import RedirectResponse
from database import get_async_session





router = APIRouter(
    prefix="/level",
    tags=["level"]
)





@router.get("/{slug}")
async def get_level(request: Request, slug: str, session: AsyncSession = Depends(get_async_session),
                    message: str = None, message_class: str = None,
                    form_message: str = None, form_message_class: str = None):

        return templates.TemplateResponse(f"menu_items/{slug}.html", {"request": request,
                                                                        'message': message, 'message_class': message_class,
                                                                        'form_message': form_message, 'form_message_class': form_message_class})


    # except Exception as e:
    #     return {
    #         "status": "error",
    #         "data": e,
    #         "details": 'По какой-то причине возникла ошибка, лучшее что вы можете сделать - написать админу'
    #     }


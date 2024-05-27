from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Form
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from backend.src.dependencies import MESSAGES_SERVICE_DEPENDENCY

router = APIRouter()


@router.post("/contact")
async def send_contact_email(
    name: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    message: Annotated[str, Form()],
    token: Annotated[str, Form()],
    messages: MESSAGES_SERVICE_DEPENDENCY,
    background_tasks: BackgroundTasks,
) -> JSONResponse:
    fast_mail = messages.get_fast_mail(name, email)
    message = messages.build_message(name, message)

    background_tasks.add_task(fast_mail.send_message, message, "contact.html")

    return JSONResponse("Email sent")

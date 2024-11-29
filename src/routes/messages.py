from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Form
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from src.dependencies import MESSAGES_SERVICE_DEPENDENCY, verify_recaptcha

router = APIRouter()


@router.post("/contact", dependencies=[Depends(verify_recaptcha)])
async def send_contact_email(
    name: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    message: Annotated[str, Form()],
    messages: MESSAGES_SERVICE_DEPENDENCY,
    background_tasks: BackgroundTasks,
) -> JSONResponse:
    fast_mail = messages.get_fast_mail(from_name=name, from_email=email)
    message = messages.build_message(from_name=name, message=message)

    background_tasks.add_task(fast_mail.send_message, message, "contact.html")

    return JSONResponse("Email sent.")

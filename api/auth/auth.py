from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import Response
from uuid import uuid4
from .session_verifier import backend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from api.configs import session_secret_key

cookie_params = CookieParameters()
cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key=session_secret_key,
    cookie_params=cookie_params,
)

class SessionData(BaseModel):
    username: str

auth_router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
)

@auth_router.post("/create_session")
async def create_session(response: Response):
    session_id = uuid4()
    data = SessionData(email="")
    await backend.create(session_id, data)
    cookie.attach_to_response(response, session_id)
    return f"created session!"

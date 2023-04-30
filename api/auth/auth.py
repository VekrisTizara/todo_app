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

@auth_router.post("/create_session/{name}")
async def create_session(response: Response):
    session = uuid4()
    data = SessionData(username="")
    await backend.create(session, data)
    cookie.attach_to_response(response, session)
    return f"created session!"

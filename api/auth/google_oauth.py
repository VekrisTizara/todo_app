
"""
from oauth2client import client
from google.oauth2 import id_token
from google.auth.transport import requests"""

from fastapi import APIRouter, Depends, HTTPException
from .google_oauth_setup import API_LOCATION
from api.configs import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from api.db import db
from .session_verifier import verifier
from .auth import cookie
from uuid import UUID

import requests
import json


gauth_router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
)

@gauth_router.get("/google_oauth_url")
async def get_google_oauth_url(session_id: UUID = Depends(cookie)):
    google_oauth_url = f'https://accounts.google.com/o/oauth2/v2/auth?' \
                       f'access_type=offline&' \
                       f'include_granted_scopes=true&' \
                       f'response_type=code&' \
                       f'redirect_uri={API_LOCATION}/auth/auth_code_callback&' \
                       f'client_id={GOOGLE_CLIENT_ID}&' \
                       f'scope=email&' \
                       f'state={session_id}'
    return google_oauth_url


@gauth_router.get("/auth_code_callback")
async def receive_auth_code_callback_and_request_token(code, state: UUID):
    session_id=state
    session = await verifier.backend.read(session_id)
    if not session:
        raise HTTPException(status_code=400, detail="Session not found")

    data = {
        "client_id" : GOOGLE_CLIENT_ID,
        "client_secret" : GOOGLE_CLIENT_SECRET,
        "code" : code,
        "redirect_uri" : f'{API_LOCATION}/auth/auth_code_callback',
        "grant_type" : "authorization_code"
    }
    token_response = requests.post('https://oauth2.googleapis.com/token', data)
    token_obj = json.loads(token_response.text)
    token = token_obj['access_token']

    # request EMAIL from gapi using token
    tokenInfoUrl = f'https://www.googleapis.com/oauth2/v2/tokeninfo?access_token={token}'
    token_info_response = requests.get(tokenInfoUrl)
    token_info = json.loads(token_info_response.text)
    user_email = token_info['email']

    # update current SESSION with the EMAIL
    session.email = user_email
    await verifier.backend.update(session_id, session)

    # if token:
    #     db.

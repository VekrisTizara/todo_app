from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import (
    OAuth2,
    OAuthFlowsModel,
    get_authorization_scheme_param,
)

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from pydantic import BaseModel

"""
from oauth2client import client
from google.oauth2 import id_token
from google.auth.transport import requests"""

from fastapi import APIRouter
from .google_oauth_setup import API_LOCATION
from api.configs import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from api.db import db

import requests
import json


router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
)

@router.get("/google_oauth_url")
async def get_google_oauth_url():
    google_oauth_url = f'https://accounts.google.com/o/oauth2/v2/auth?' \
                       f'access_type=offline&' \
                       f'include_granted_scopes=true&' \
                       f'response_type=code&' \
                       f'redirect_uri={API_LOCATION}/auth/auth_code_callback&' \
                       f'client_id={GOOGLE_CLIENT_ID}&' \
                       f'scope=https://www.googleapis.com/auth/userinfo.email'
    return google_oauth_url


@router.get("/auth_code_callback")
async def receive_auth_code_callback_and_request_token(code):
    data = {
        "client_id" : GOOGLE_CLIENT_ID,
        "client_secret" : GOOGLE_CLIENT_SECRET,
        "code" : code,
        "redirect_uri" : f'{API_LOCATION}/auth/auth_code_callback',
        "grant_type" : "authorization_code"
    }
    response = requests.post('https://oauth2.googleapis.com/token', data)
    print(code)
    print(response.url)
    print(response.headers)
    print(response.status_code)

    json_response = json.loads(response.text)
    token = json_response['access_token']

    print(token)
    # request EMAIL from gapi using token
    # get current SESSION
    # update current SESSION with the EMAIL

    # if token:
    #     db.




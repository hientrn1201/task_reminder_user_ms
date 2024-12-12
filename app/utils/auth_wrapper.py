import requests
from fastapi import Request, HTTPException
from app.config import settings

VERIFY_TOKEN_URL = f"{settings.USER_SERVICE_URL}/verify_token"


def login_required(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Authorization header missing")

    # Verify token via user service
    # response = requests.get(VERIFY_TOKEN_URL, headers={
    #                         "Authorization": auth_header})
    # if response.status_code != 200:
    #     raise HTTPException(status_code=response.status_code,
    #                         detail=response.json().get("error", "Unauthorized"))

    # Pass user info to the wrapped function
    # user_info = response.json()
    # request.state.user_id = user_info['user_id']

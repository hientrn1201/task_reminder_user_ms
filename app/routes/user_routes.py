# app/routes/user_routes.py

from fastapi import APIRouter, HTTPException
from app.config import settings
import requests  # Use requests for synchronous HTTP calls

router = APIRouter()


@router.get("/{user_id}")
def get_user(user_id: int):
    url = f"{settings.USER_SERVICE_URL}/users/{user_id}"
    print(url)
    # DUMMY var I used so I don't have to set up user microservice
    js = {
        'user_id': '123',
        'username': 'Nguyen',
        'email': 'nqt2001@columbia.edu',
    }
    print(js)

    try:
        response = requests.get(url)  # Synchronous GET request
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    return response.json()  # Return the JSON response

from fastapi import APIRouter, HTTPException, Request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request as GoogleRequest
from fastapi.responses import RedirectResponse
from app.config import settings
import requests
import os
import pathlib

router = APIRouter()

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent.parent, "client-secret.json"
)

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri=f"{settings.COMPOSITE_SERVICE_URL}/auth/callback",
)


@router.get("/auth/google")
async def google_auth():
    """Initiate Google OAuth flow."""
    authorization_url, state = flow.authorization_url()
    return {"auth_url": authorization_url}


@router.get("/auth/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback."""
    try:
        flow.fetch_token(authorization_response=str(request.url))
        credentials = flow.credentials
        token_request = GoogleRequest()

        # Validate the ID token
        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID,
        )

        # Prepare user payload
        email = id_info.get("email")
        name = id_info.get("name", "Anonymous")
        payload = {"name": name, "email": email, "auth_provider": "GOOGLE"}

        # Interact with user service
        user_service_url = f"{settings.USER_SERVICE_URL}/users/register"
        response = requests.post(user_service_url, json=payload)
        response.raise_for_status()
        user = response.json()

        # Generate JWT token
        jwt_token = requests.post(
            f"{settings.USER_SERVICE_URL}/generate_jwt", json=user
        ).json()["jwt"]

        # Redirect to frontend with token
        return RedirectResponse(f"{settings.FRONTEND_URL}?jwt={jwt_token}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# app/routes/reminder_routes.py

from fastapi import APIRouter, HTTPException
from app.config import settings
from app.utils.http_client import http_client

router = APIRouter()



@router.get("/upcoming")
async def get_upcoming_reminders():
    url = f"{settings.REMINDER_SERVICE_URL}/api/reminders/grouped"
    res = await http_client.fetch(url)
    return res


@router.get("/{reminder_id}")
async def get_reminder(reminder_id: int):
    url = f"{settings.REMINDER_SERVICE_URL}/api/reminders/{reminder_id}"
    return await http_client.fetch(url)




@router.post("/")
async def create_reminder(reminder_data: dict):
    url = f"{settings.REMINDER_SERVICE_URL}/api/reminders"
    return await http_client.fetch(url, method="POST", json_data=reminder_data)

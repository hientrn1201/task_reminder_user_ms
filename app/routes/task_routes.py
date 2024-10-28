# app/routes/task_routes.py

from fastapi import APIRouter, HTTPException
from app.config import settings
from app.utils.http_client import http_client

router = APIRouter()


@router.get("/{task_id}")
async def get_task(task_id: int):
    url = f"{settings.TASK_SERVICE_URL}/tasks/{task_id}"
    return await http_client.fetch(url)


@router.post("/")
async def create_task(task_data: dict):
    url = f"{settings.TASK_SERVICE_URL}/tasks"
    return await http_client.fetch(url, method="POST", json_data=task_data)

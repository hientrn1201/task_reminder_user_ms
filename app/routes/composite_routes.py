# app/routes/composite_routes.py

from fastapi import APIRouter, HTTPException
from app.config import settings
from app.utils.http_client import http_client
import asyncio

router = APIRouter()


@router.post("/task-with-reminder")
async def create_task_with_reminder(task_data: dict, reminder_data: dict):
    task_url = f"{settings.TASK_SERVICE_URL}/tasks"
    reminder_url = f"{settings.REMINDER_SERVICE_URL}/reminders"

    async with httpx.AsyncClient() as client:
        # Attempt to create the task asynchronously
        task_response = await client.post(task_url, json=task_data)
        if task_response.status_code != 201:
            raise HTTPException(
                status_code=task_response.status_code, detail="Failed to create task")

        # Retrieve the task ID for reminder association and potential rollback
        task_id = task_response.json().get("task_id")
        # Associate the reminder with the created task
        reminder_data["task_id"] = task_id

        # Attempt to create the reminder asynchronously
        reminder_response = await client.post(reminder_url, json=reminder_data)
        if reminder_response.status_code != 201:
            # Roll back the task if reminder creation fails
            rollback_response = await client.delete(f"{task_url}/{task_id}")
            if rollback_response.status_code != 204:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create reminder and task rollback was unsuccessful"
                )
            raise HTTPException(
                status_code=reminder_response.status_code, detail="Failed to create reminder")

    # Return the responses if both operations succeed
    return {"task": task_response.json(), "reminder": reminder_response.json()}

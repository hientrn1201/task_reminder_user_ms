# app/routes/task_routes.py

from fastapi import APIRouter, HTTPException, Depends
from app.config import settings
from app.utils.http_client import http_client
from app.utils.auth_wrapper import login_required
from fastapi import Request

router = APIRouter()


@router.get("", dependencies=[Depends(login_required)])
# @login_required
async def get_tasks(request: Request):
    # user_id = request.state.user_id  # Extract the user_id from request.state
    # print(user_id)
    user_id = 1
    url = f"{settings.TASK_SERVICE_URL}/tasks?user_id={user_id}"
    return await http_client.fetch(url)


@router.get("/{task_id}")
# @login_required
async def get_task(task_id: int, request: Request):
    url = f"{settings.TASK_SERVICE_URL}/tasks/{task_id}"
    return await http_client.fetch(url)


@router.put('/{task_id}')
# @login_required
async def put_task(task_id: int, task_data: dict, request: Request):
    url = f"{settings.TASK_SERVICE_URL}/tasks/{task_id}"
    return await http_client.fetch(url, method="PUT", json_data=task_data)


@router.post("/")
# @login_required
async def create_task(task_data: dict, request: Request):
    url = f"{settings.TASK_SERVICE_URL}/tasks"
    return await http_client.fetch(url, method="POST", json_data=task_data)

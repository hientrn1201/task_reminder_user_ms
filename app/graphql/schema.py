import strawberry
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from app.utils.http_client import http_client
from app.config import settings


# Define GraphQL types

@strawberry.type
class TaskType:
    task_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[str]  # DateTime as string (ISO format)
    created_at: str  # DateTime as string (ISO format)
    updated_at: str  # DateTime as string (ISO format)


@strawberry.type
class UserType:
    user_id: int
    username: str
    email: str


@strawberry.type
class ReminderType:
    reminder_id: int
    task_id: int
    user_id: int
    reminder_time: str
    message: str


# Define GraphQL Queries

@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, user_id: int) -> UserType:
        url = f"{settings.USER_SERVICE_URL}/user?user_id={user_id}"
        user_data = await http_client.fetch(url)
        return UserType(**user_data)

    @strawberry.field
    async def get_tasks(self, user_id: int, page: int = 1, size: int = 10) -> List[TaskType]:
        url = f"{settings.TASK_SERVICE_URL}/tasks/?user_id={user_id}&page={page}&size={size}"
        task_data = await http_client.fetch(url)

        # Log the task_data to verify the response
        print(f"Fetched task data: {task_data}")

        if "items" not in task_data:
            return []

        task_list = [
            TaskType(
                task_id=task["task_id"],
                title=task["title"],
                description=task.get("description"),
                status=task["status"],
                priority=task["priority"],
                due_date=task.get("due_date"),
                created_at=task["created_at"],
                updated_at=task["updated_at"],
            )
            for task in task_data["items"]
        ]
        return task_list

    @strawberry.field
    async def get_reminders(self, user_id: int) -> List[ReminderType]:
        url = f"{settings.REMINDER_SERVICE_URL}/reminders/grouped"
        reminders_data = await http_client.fetch(url)
        user_reminders = [
            ReminderType(**reminder)
            for reminder_group in reminders_data["reminders"]
            if reminder_group["user_id"] == user_id
            for reminder in reminder_group["tasks"]
        ]
        return user_reminders


# Define GraphQL Schema
schema = strawberry.Schema(query=Query)

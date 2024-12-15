from fastapi import APIRouter, HTTPException,status
from app.config import settings
from app.utils.http_client import http_client
import json
import asyncio
import redis.asyncio as aioredis
from starlette.responses import JSONResponse

router = APIRouter()
async def publish_update_task(task_id: int,task_data: dict):
    try:
        print('hi')
        redis_connection = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        input = {}
        input['task_id'] = task_id
        input['task_data'] = task_data
        message = json.dumps(task_data)
        await redis_connection.rpush("task_queue", json.dumps(input))
        await redis_connection.close()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Task update accepted."})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to publish")
    

@router.post("/publish-update/{task_id}")
async def publish_update(task_id: int,task_data: dict):
    await publish_update_task(task_id,task_data)
    return "published successfully"
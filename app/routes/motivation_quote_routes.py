# app/routes/user_routes.py

from fastapi import APIRouter, HTTPException
from app.utils.http_client import http_client

router = APIRouter()


@router.get("/")
async def get_random_quote():
    url = "https://zenquotes.io/api/random"
    quote_data = await http_client.fetch(url)
    if quote_data:
        quote = quote_data[0].get('q')  # The quote text
        author = quote_data[0].get('a')  # The author
        return {"quote": quote, "author": author}
    return {"error": "Unable to fetch quote"}

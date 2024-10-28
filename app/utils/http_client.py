# app/utils/http_client.py

import httpx


class HttpClient:
    async def fetch(self, url: str, method: str = "GET", json_data=None):
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, json=json_data)
            response.raise_for_status()
            return response.json()


http_client = HttpClient()

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_cache.decorator import cache

from starlette import status

from app.config_reader import app
from app.services.url_service import url_service


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/short_url")
async def url_endpoint(request: Request):
    request_json = await request.json()
    long_url = request_json.get("url", None)

    response = await url_service.create_or_get(long_url)

    return JSONResponse(response.data, response.status)


@app.get("/{slug}")
async def redirect_endpoint(slug: str):
    response = await url_service.get_by_slug(slug)

    if response.status == 302:
        return RedirectResponse(
            url=response.data.get("long_url", "/"),
            status_code=status.HTTP_302_FOUND
        )

    return JSONResponse(response.data, response.status)

# HTTP

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from redis import Redis

from .models import TimeAdvance
from .service import TimeService
from core.cache import get_cache

router = APIRouter()


@router.get("")
def get_time(cache: Redis = Depends(get_cache)):
    time_service = TimeService(cache)

    return JSONResponse(
        content=jsonable_encoder({"current_date": time_service.get_time()}),
        status_code=200
    )


@router.post("/advance")
def set_time(time_advance: TimeAdvance, cache: Redis = Depends(get_cache)):
    time_service = TimeService(cache)
    time = time_service.set_time(time_advance.current_date)

    return JSONResponse(
        content=jsonable_encoder({"current_date": time}),
        status_code=200
    )
# HTTP

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

from redis import Redis
from sqlalchemy.orm import Session

from .repository import BanWordsRepository
from core.database import get_db
from core.cache import get_cache

router = APIRouter() # /moderation

@router.post("/active")
def switch_moderation(
    status: bool = Body(..., embed=True),
    cache: Redis = Depends(get_cache),
):
    cache.setex(
        name="moderate",
        value=f"{status}",
        time=int(10e10) # Бесконечный ключ
    )

    return JSONResponse(
        content={"status": f"switched moderation to {status}"}, 
        status_code=200
    )

@router.post("/strict")
def switch_strict_moderation(
    status: bool = Body(..., embed=True),
    cache: Redis = Depends(get_cache),
):
    cache.setex(
        name="moderate_strict",
        value=f"{status}",
        time=int(10e10) # Бесконечный ключ
    )

    return JSONResponse(
        content={"status": f"switched strict moderation to {status}"}, 
        status_code=200
    )


@router.post("/banwords")
def add_banword(
    banword: str = Body(..., embed=True), 
    db: Session = Depends(get_db),
):
    repository = BanWordsRepository(db)
    result = repository.add_banword(banword)

    if not result:
        return JSONResponse(
            content={"error": "banword has already been added"},
            status_code=409
        )
    
    return JSONResponse(
        content={"status": "banword was added"},
        status_code=201
    )


@router.get("/banwords")
def get_banwords(
    db: Session = Depends(get_db),
):
    repository = BanWordsRepository(db)
    banwords = repository.get_banned_words()
    
    return JSONResponse(
        content={"banwords": banwords},
        status_code=200
    )

@router.delete("/banwords")
def delete_banword(
    banword: str = Body(..., embed=True), 
    db: Session = Depends(get_db),
):
    repository = BanWordsRepository(db)
    status = repository.delete_banword(banword)
    
    if not status:
        return HTTPException(
            detail="banword not found",
            status_code=404
        )

    return JSONResponse(
        content={"status": "banword deleted"},
        status_code=204
    )

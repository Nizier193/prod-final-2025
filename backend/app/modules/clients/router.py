# HTTP

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing import List, Dict
from sqlalchemy.orm import Session
from uuid import UUID

from .repository import ClientRepository
from .models import Client
from core.database import get_db

router = APIRouter()


@router.post("/bulk")
def create_clients(clients: List[Client], db: Session = Depends(get_db)):
    repository = ClientRepository(db)

    client_ids = [client.client_id for client in clients]
    all_existing_ids = repository.get_all_client_ids()

    result_clients: List[Dict] = []
    for client_id, client in zip(client_ids, clients):

        if client_id in all_existing_ids:               # Делаем апдейт
            result = repository.update_client(client)
        else:                                           # Добавляем клиента
            result = repository.insert_client(client)

        result_clients.append(result.to_dict())

    return JSONResponse(
        content=jsonable_encoder(result_clients),
        status_code=201
    )


@router.get("/{clientId}")
def get_client(clientId: UUID, db: Session = Depends(get_db)):
    repository = ClientRepository(db)

    client = repository.get_client_by_id(clientId)
    
    return JSONResponse(
        content=jsonable_encoder(client),
        status_code=200
    )

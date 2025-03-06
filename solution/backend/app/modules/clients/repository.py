# Работа с БД
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select

from .schemas import clients, metadata
from .models import Client

class ClientRepository():
    def __init__(self, db):
        self.db = db
        metadata.create_all(db.bind) # Создание базы


    def get_all_client_ids(self) -> List[UUID]:
        query = select(clients)
        result = self.db.execute(query).mappings().fetchall()
        ids = [dict(r).get("client_id") for r in result]

        return ids
    

    def get_client_by_id(self, id: UUID) -> Optional[Client]:
        query = select(clients).where(clients.c.client_id == id)
        result = self.db.execute(query).mappings().fetchone()

        if not result:
            return None

        return Client.model_validate(dict(result))
    

    def insert_client(self, client: Client) -> Client:
        model_dict = client.to_dict()
        query = clients.insert().values(**model_dict)
        self.db.execute(query)
        self.db.commit()

        return Client.model_validate(model_dict)


    def update_client(self, client: Client) -> Client:
        model_dict = client.to_dict()
        query = (
            clients.update()
            .where(clients.c.client_id == client.client_id)
            .values(**model_dict)
        )
        self.db.execute(query)
        self.db.commit()
        
        return self.get_client_by_id(client.client_id)

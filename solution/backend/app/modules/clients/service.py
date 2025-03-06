# Бизнес логика

from uuid import UUID
from .repository import ClientRepository
from sqlalchemy.orm import Session

# Сервисный модуль для Dependency Injection
class ClientRepositoryService():
    def __init__(self, db: Session) -> None:
        self.repository = ClientRepository(db)


    def get_client_by_id(self, client_id: UUID):
        return self.repository.get_client_by_id(client_id)
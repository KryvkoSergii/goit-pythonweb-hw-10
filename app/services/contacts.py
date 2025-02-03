from sqlalchemy.ext.asyncio import AsyncSession
from repository.contacts import ContactRepository
from schemas import ContactsQuery, ContractModel, ContactBase
from repository.models import Contact
from logging import Logger
from typing import List
from errors import ContactNotFoundError
from datetime import datetime


class ContactService:
    def __init__(self, logger: Logger, db: AsyncSession):
        self.__contact_repository: ContactRepository = ContactRepository(db)
        self.__logger: Logger = logger

    async def get_by_query(self, query: ContactsQuery) -> List[ContractModel]:
        self.__logger.debug(f"searching for contacts by '{query}'")
        entities = await self.__contact_repository.get_list_by_query(query)
        return list(
            map(lambda c: self.__transform_contact_to_contract_model(c), entities)
        )

    async def get_by_id(self, id: int):
        self.__logger.debug(f"searching for contact by id: '{id}'")
        contact = await self.__contact_repository.get_by_id(id)
        return self.__transform_contact_to_contract_model(contact)

    async def create(self, contact: ContactBase):
        self.__logger.info(f"creating contact: '{contact}'")
        date = None
        if contact.date:
            date = datetime.strptime(contact.date, "%Y-%m-%d").date()

        entity = Contact(
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            phone=contact.phone,
            date=date,
            notes=contact.notes,
        )

        contact = await self.__contact_repository.create(entity)
        return self.__transform_contact_to_contract_model(contact)

    async def update(self, id: int, contact: ContractModel):
        self.__logger.info(f"updating contact by id: '{id}' content: '{contact}'")
        if id != contact.id:
            raise ValueError(
                f"Id in request mismatch. Request: '{id}', body: '{contact.id}'"
            )

        persisted = await self.__contact_repository.get_by_id(id)
        if not persisted:
            raise ContactNotFoundError(id)

        for key, value in contact.__dict__.items():
            if key == "date":
                value = (
                    datetime.strptime(contact.date, "%Y-%m-%d").date()
                    if contact.date
                    else None
                )
            setattr(persisted, key, value)

        contact = await self.__contact_repository.update(persisted)
        return self.__transform_contact_to_contract_model(contact)

    async def remove(self, id: int) -> ContractModel:
        self.__logger.info(f"remove contact by id: '{id}'")
        persisted = await self.__contact_repository.get_by_id(id)
        if not persisted:
            raise ContactNotFoundError(id)
        await self.__contact_repository.remove(persisted)
        return self.__transform_contact_to_contract_model(persisted)

    def __transform_contact_to_contract_model(self, contact: Contact) -> ContractModel:
        return ContractModel(
            id=contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            email=contact.email,
            phone=contact.phone,
            date=contact.date.isoformat(),
            notes=contact.notes,
        )

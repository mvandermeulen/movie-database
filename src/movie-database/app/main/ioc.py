from contextlib import asynccontextmanager
from typing import AsyncIterator

from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.commands.registration.register import Register
from app.application.commands.adding_task.create_task import CreateAddingTask
from app.application.commands.movie.create_movie import CreateMovie
from app.application.queries.auth.login import Login
from app.application.queries.user.get_current_user import GetCurrentUser
from app.infrastructure.database.factory import DatabaseFactoryManager
from app.infrastructure.message_broker.factory import EventBusFactory
from app.infrastructure.uow import UnitOfWorkImpl
from app.presentation.handler_factory import HandlerFactory


class IoC(HandlerFactory):

    def __init__(
        self,
        db_factory_manager: DatabaseFactoryManager,
        event_bus_factory: EventBusFactory
    ) -> None:
        self.db_factory_manager = db_factory_manager
        self.event_bus_factory = event_bus_factory

    @asynccontextmanager
    async def register(self) -> AsyncIterator[Register]:
        async with self.db_factory_manager.build_repo_factory() as repo_factory:
            yield Register(
                user_repo=repo_factory.build_user_repo(),
                uow=UnitOfWorkImpl(await repo_factory.build_uow())
            )
    
    @asynccontextmanager
    async def create_adding_task(
        self, identity_provider: IdentityProvider
    ) -> AsyncIterator[CreateAddingTask]:
        async with (
            self.db_factory_manager.build_repo_factory() as repo_factory,
            self.event_bus_factory.build_event_bus() as event_bus
        ):
            yield CreateAddingTask(
                adding_task_repo=repo_factory.build_adding_task_repo(),
                identity_provider=identity_provider,
                event_bus=event_bus,
                uow=UnitOfWorkImpl(await repo_factory.build_uow(), await event_bus.build_uow())
            )
    
    @asynccontextmanager
    async def create_movie(self) -> AsyncIterator[CreateMovie]:
        async with self.db_factory_manager.build_repo_factory() as repo_factory:
            yield CreateMovie(
                movie_repo=repo_factory.build_movie_repo(),
                uow=UnitOfWorkImpl(await repo_factory.build_uow())
            )

    @asynccontextmanager
    async def login(self) -> AsyncIterator[Login]:
        async with self.db_factory_manager.build_reader_factory() as reader_factory:
            yield Login(auth_reader=reader_factory.build_auth_reader())
    
    @asynccontextmanager
    async def get_current_user(
        self, identity_provider: IdentityProvider
    ) -> AsyncIterator[GetCurrentUser]:
        async with self.db_factory_manager.build_reader_factory() as reader_factory:
            yield GetCurrentUser(
                user_reader=reader_factory.build_user_reader(),
                identity_provider=identity_provider
            )

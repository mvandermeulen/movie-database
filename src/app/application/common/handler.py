from abc import ABC, abstractmethod
from typing import TypeVar


InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class Handler(ABC):

    @abstractmethod
    async def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


HandlerT = TypeVar("HandlerT", bound=Handler)


class CommandHandler(Handler):
    ...


CommandHandlerT = TypeVar("CommandHandlerT", bound=CommandHandler)


class QueryHandler(Handler):
    ...


QueryHandlerT = TypeVar("QueryHandlerT", bound=QueryHandler)
from typing import TypeVar, Generic, AsyncContextManager
from abc import ABC, abstractmethod


Handler = TypeVar("Handler")


class HandlerFactory(ABC, Generic[Handler]):
    
    @abstractmethod
    async def create_handler(self) -> AsyncContextManager[Handler]:
        """
        Setups dependencies to handler and returns it.
        
        Example:

        .. code-block::python
        async with some_handler_factory.create_handler() as handle:
            await handle(SomeHandlerDTO()) 
        """
        raise NotImplementedError

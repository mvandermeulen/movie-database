import asyncio
from logging import getLogger
from dataclasses import dataclass

from src.application.common import utils
from src.application.common import mixins
from . import dto
from . import errors
from . import interfaces


logger = getLogger("ConfirmUser")


@dataclass(frozen=True, slots=True)
class ConfirmUser(mixins.SupportsGetAndCacheUser):

    db_gateway: interfaces.DatabaseGateway
    cb_gateway: interfaces.CachebaseGateway
    tq_gateway: interfaces.TaskQueueGateway

    @utils.handle_unexpected_exceptions(
        logger, errors.UserDoesNotExistError, errors.UserAlreadyConfirmedError
    )
    async def __call__(self, data: dto.ConfirmUserDTO) -> None:
        # 1.Get user
        user = await self.get_and_cache_user(
            db_gateway=self.db_gateway, cb_gateway=self.cb_gateway,
            email=data.email
        )
        if user is None:
            raise errors.UserDoesNotExistError()
        
        # 2.Ensure user is not confirmed
        if user.is_confirmed:
            raise errors.UserAlreadyConfirmedError()
        
        # 3.Confirm user
        user.confirm()

        # 4.Save changes and enqueue `send_greeting_email` task
        await asyncio.gather(
            self.db_gateway.update_user(user), self.cb_gateway.update_user(user),
            self.tq_gateway.enqueue_send_greeting_email_task(user_id=user.id)
        )
        await asyncio.gather(
            self.db_gateway.commit(), self.cb_gateway.commit(), self.tq_gateway.commit()
        )
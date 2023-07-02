from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.domain.models.user.model import User
from src.domain.models.user.value_objects import UserId, Username
from src.application.common.result import Result
from src.application.common.interfaces.passoword_encoder import PasswordEncoder
from .command import RegisterCommand, RegisterCommandResult
from .interfaces import RegisterCommandDBGateway
from .errors import UsernameAlreadyExistsError


CommandHandlerResult = (
    Result[RegisterCommandResult, None] |
    Result[None, UsernameAlreadyExistsError]
)


@dataclass(frozen=True, slots=True)
class RegisterCommandHandler:

    db_gateway: RegisterCommandDBGateway
    password_encoder: PasswordEncoder

    def __call__(self, command: RegisterCommand) -> CommandHandlerResult:
        username = Username(command.username)
        user = self.db_gateway.get_user_by_username(
            username=username
        )
        if user is not None:
            error = UsernameAlreadyExistsError(username.value)
            return Result(value=None, error=error)
        
        user_id = UserId(uuid4())
        encoded_password = self.password_encoder.encode(
            password=command.password
        )
        user = User.create(
            user_id=user_id,
            username=username,
            password=encoded_password,
            created_at=datetime.utcnow()
        )

        self.db_gateway.save_user(user)
        self.db_gateway.commit()

        command_result = RegisterCommandResult(user_id.value)
        result = Result(value=command_result, error=None)

        return result

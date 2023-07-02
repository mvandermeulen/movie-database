from dataclasses import dataclass

from src.presentation.api.interactor import ApiInteractor
from src.application.common.interfaces.database_gateway import (
    DatabaseGateway
)
from src.application.common.interfaces.passoword_encoder import (
    PasswordEncoder
)
from src.application.commands.register.command import (
    RegisterCommand
)
from src.application.commands.register.handler import (
    RegisterCommandHandler,
    CommandHandlerResult as RegisterCommandHandlerResult
)
from src.application.commands.rate_movie.command import (
    RateMovieCommand
)
from src.application.commands.rate_movie.handler import (
    RateMovieCommandHandler,
    CommandHandlerResult as RateMovieCommandHandlerResult
)
from src.application.commands.reevaluate_movie.command import (
    ReevaluateMovieCommand
)
from src.application.commands.reevaluate_movie.handler import (
    ReevaluateMovieCommandHandler,
    CommandHandlerResult as ReevaluateMovieCommandHandlerResult
)
from src.application.commands.remove_user_movie_rating.command import (
    RemoveUserMovieRatingCommand
)
from src.application.commands.remove_user_movie_rating.handler import (
    RemoveUserMovieRatingCommandHandler,
    CommandHandlerResult as RemoveUserMovieRatingCommandHandlerResult
)
from src.application.queries.login.query import (
    LoginQuery
)
from src.application.queries.login.handler import (
    LoginQueryHandler,
    QueryHanlderResult as LoginQueryHandlerResult
)
from src.application.queries.username_existence.query import (
    CheckUsernameExistenceQuery
)
from src.application.queries.username_existence.handler import (
    CheckUsernameExistenceQueryHandler,
    QueryHandlerResult as CheckUsernameExistenceQueryHandlerResult
)
# FIXME: Simplify imports

@dataclass(frozen=True, slots=True)
class ApiInteractorImpl(ApiInteractor):

    db_gateway: DatabaseGateway
    password_encoder: PasswordEncoder

    def handle_register_command(
        self,
        command: RegisterCommand
    ) -> RegisterCommandHandlerResult:
        handler = RegisterCommandHandler(
            db_gateway=self.db_gateway,
            password_encoder=self.password_encoder
        )
        return handler(command)

    def handle_rate_movie_command(
        self,
        command: RateMovieCommand
    ) -> RateMovieCommandHandlerResult:
        handler = RateMovieCommandHandler(
            db_gateway=self.db_gateway
        )
        return handler(command)
    
    def handle_reevaluate_movie_command(
        self,
        command: ReevaluateMovieCommand
    ) -> ReevaluateMovieCommandHandlerResult:
        handler = ReevaluateMovieCommandHandler(
            db_gateway=self.db_gateway
        )
        return handler(command)
    
    def handle_remove_user_movie_rating_command(
        self,
        command: RemoveUserMovieRatingCommand
    ) -> RemoveUserMovieRatingCommandHandlerResult:
        handler = RemoveUserMovieRatingCommandHandler(
            db_gateway=self.db_gateway
        )
        return handler(command)

    def handle_login_query(
        self,
        query: LoginQuery
    ) -> LoginQueryHandlerResult:
        handler = LoginQueryHandler(
            db_gateway=self.db_gateway,
            password_encoder=self.password_encoder
        )
        return handler(query)

    def handle_check_username_existence_query(
        self,
        query: CheckUsernameExistenceQuery
    ) -> CheckUsernameExistenceQueryHandlerResult:
        hanlder = CheckUsernameExistenceQueryHandler(
            db_gateway=self.db_gateway
        )
        return hanlder(query)
    
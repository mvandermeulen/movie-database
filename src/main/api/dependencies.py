from fastapi import FastAPI

from src.presentation.api.interactor import ApiInteractor
from src.presentation.api.authenticator import ApiAuthenticator
from src.infrastructure.psycopg.psycopg import get_psycopg2_connection
from src.infrastructure.psycopg.gateway import PsycopgDatabaseGateway
from src.infrastructure.password_encoder import HashlibPasswordEncoder
from src.infrastructure.auth.api import ApiAuthenticatorImpl
from .config import AuthConfig, PostgresConfig
from .interactor import ApiInteractorImpl



def setup_dependencies(
    app: FastAPI,
    auth_config: AuthConfig,
    postgres_config: PostgresConfig
) -> None:
    psycopg_conn = get_psycopg2_connection(postgres_config.dsn)
    psycopg_db_gateway = PsycopgDatabaseGateway(psycopg_conn)
    password_encoder = HashlibPasswordEncoder()

    api_interactor = ApiInteractorImpl(
        db_gateway=psycopg_db_gateway,
        password_encoder=password_encoder
    )
    authenticator = ApiAuthenticatorImpl(
        secret=auth_config.auth_secret,
        access_token_expires=auth_config.auth_access_token_expires,
        algorithm=auth_config.auth_algorithm
    )

    app.dependency_overrides[ApiInteractor] = lambda: api_interactor
    app.dependency_overrides[ApiAuthenticator] = lambda: authenticator
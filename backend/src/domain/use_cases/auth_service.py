from src.infastructure.repositories.auth_repository import AuthRepository
from src.domain.interfaces.auth_interface import AuthInterface


class AuthenticationService:

    def __call__(self) -> AuthInterface:
        return self

    def __init__(self, auth_repository=AuthRepository):
        self.auth_repository = auth_repository()

    def authenticate_user(self, code: str):
        return self.auth_repository.authenticate_user(code)

    def verifiy_the_login(self, token: str):
        return self.auth_repository.verifiy_the_login(token)

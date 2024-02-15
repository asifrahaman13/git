# src/core/use_cases/user_service.py

from src.domain.interfaces.user_interface import UserInterface
from src.infastructure.repositories.user_repository import UserRepository


class UserService(UserInterface):
    def __call__(self) -> UserInterface:
        return self

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def fetch_all_respositories(self, token):
        return self.user_repository.fetch_all_respositories(token)

    def fetch_all_dependencies(self, token, repo):
        return self.user_repository.fetch_all_dependencies(token, repo)

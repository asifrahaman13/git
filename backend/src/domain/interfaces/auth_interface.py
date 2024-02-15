# src/core/interfaces/user_interface.py
from abc import ABC, abstractmethod


class AuthInterface(ABC):

    @abstractmethod
    def authenticate_user(self, code):
        pass

    @abstractmethod
    def verifiy_the_login(self, token):
        pass

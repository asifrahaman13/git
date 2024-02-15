# src/core/interfaces/user_interface.py
from abc import ABC, abstractmethod


class UserInterface(ABC):

    @abstractmethod
    def fetch_all_respositories(self, token):
        pass

    @abstractmethod
    def fetch_all_dependencies(self, token):
        pass

from __future__ import annotations
from abc import abstractmethod


class Command:

    @abstractmethod
    def excecute(self) -> None:
        pass

    @abstractmethod
    def stop(self):
        pass

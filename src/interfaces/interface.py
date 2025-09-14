from abc import ABC, abstractmethod
from typing import Callable
from PIL import Image
from src.interfaces.events import InterfaceEvents


class Interface(ABC):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._listeners: list[Callable[[InterfaceEvents], None]] = []

    def _trigger_event(self, event: InterfaceEvents) -> None:
        for listener in self._listeners:
            listener(event)

    def add_listener(self, listener: Callable[[InterfaceEvents], None]) -> None:
        self._listeners.append(listener)

    @abstractmethod
    def update(self, image: Image.Image) -> None:
        pass

    @abstractmethod
    def cleanup(self) -> None:
        pass

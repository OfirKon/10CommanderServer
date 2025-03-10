from typing import List, Optional
import select
from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def fileno(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def handle(self) -> None:
        raise NotImplementedError()

class Reactor:
    _instance: Optional["Reactor"] = None

    def __init__(self):
        if self.__class__._instance is not None:
            raise RuntimeError("Cannot create second reactor instance!")
        self.__class__._instance = self
        self.handlers: List[Handler] = []
        self.should_stop = True
        self.is_running = False

    @classmethod
    def instance(cls) -> "Reactor":
        if cls._instance is None:
            raise RuntimeError("No reactor instance!")
        return cls._instance

    def add(self, obj: Handler):
        self.handlers.append(obj)

    def remove(self, obj: Handler):
        self.handlers.remove(obj)

    def run(self):
        if self.is_running:
            return
        try:
            self.should_stop = False
            self.is_running = True
            while not self.should_stop:
                self.handlers = [handler for handler in self.handlers if handler.fileno() > 0]
                try:
                    result, _, _ = select.select(self.handlers, [], [])
                    print(result)
                except ValueError:
                    pass
                else:
                    for handler in result:
                        handler.handle()
        finally:
            self.is_running = False

    def stop(self):
        self.should_stop = True

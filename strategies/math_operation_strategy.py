from abc import ABC, abstractmethod

class MathOperationStrategy(ABC):
    @abstractmethod
    def execute(self, *objects):
        pass

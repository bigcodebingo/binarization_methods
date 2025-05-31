from abc import ABC, abstractmethod
import numpy as np

class Binarizer(ABC):

    @abstractmethod
    def threshold(self, image: np.ndarray) -> np.ndarray:
        """
        Применяет алгоритм бинаризации к изображению.

        """
        pass
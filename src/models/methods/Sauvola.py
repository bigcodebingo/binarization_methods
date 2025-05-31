import numpy as np
from src.models.ImageProcessor import ImageProcessor
from src.models.Binarizer import Binarizer

class Sauvola(Binarizer):
    def __init__(self, window_size=15, k=0.2, R=128):
        self.window_size = window_size
        self.k = k
        self.R = R

    def threshold(self, image):
        image_gray = ImageProcessor.to_gray(image)
        height, width = ImageProcessor.get_size(image_gray)
        padding = self.window_size // 2
        padded_image = np.pad(image_gray, ((padding, padding), (padding, padding)), mode='edge')

        result_image = np.zeros_like(image_gray, dtype=np.uint8)

        for y in range(padding, height + padding):
            for x in range(padding, width + padding):
                window = padded_image[y - padding:y + padding + 1, x - padding:x + padding + 1]

                m = np.mean(window)
                s = np.std(window)

                threshold = m * (1 + self.k * ((s / self.R) - 1))

                if image_gray[y - padding, x - padding] > threshold:
                    result_image[y - padding, x - padding] = 255

        return result_image

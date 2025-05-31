import numpy as np
import cv2
from src.models.ImageProcessor import ImageProcessor
from src.models.Binarizer import Binarizer

class Bradley(Binarizer):
    def __init__(self, window_ratio=1/8, t=0.15):
        self.t = t
        self.window_ratio = window_ratio

    def threshold(self, image):
        image_gray = ImageProcessor.to_gray(image)
        height, width = ImageProcessor.get_size(image_gray)
        window_size = int(width * self.window_ratio)

        integral_image = cv2.integral(image_gray)

        result_image = np.zeros_like(image_gray, dtype=np.uint8)
        half = window_size // 2

        for y in range(height):
            for x in range(width):
                x1 = max(x - half, 0)
                y1 = max(y - half, 0)
                x2 = min(x + half, width - 1)
                y2 = min(y + half, height - 1)

                sum_ = (integral_image[y2 + 1, x2 + 1]
                        - integral_image[y1, x2 + 1]
                        - integral_image[y2 + 1, x1]
                        + integral_image[y1, x1])

                count = (x2 - x1 + 1) * (y2 - y1 + 1)
                mean = sum_ / count

                if image_gray[y, x] < mean * (1 - self.t):
                    result_image[y, x] = 0
                else:
                    result_image[y, x] = 255

        return result_image

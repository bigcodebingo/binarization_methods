import numpy as np
from src.models.ImageProcessor import ImageProcessor
import cv2
from src.models.Binarizer import Binarizer

class WolfJolion(Binarizer):
    def __init__(self, window_size=15, k=0.5):
        self.window_size = window_size
        self.k = k

    def threshold(self, image):
        image_gray = ImageProcessor.to_gray(image).astype(np.float64)
        height, width = ImageProcessor.get_size(image_gray)

        integral = cv2.integral(image_gray)
        integral_sq = cv2.integral(np.square(image_gray))

        half = self.window_size // 2

        x, y = np.meshgrid(np.arange(width), np.arange(height))
        x1 = (x - half).clip(0, width - 1)
        x2 = (x + half).clip(0, width - 1)
        y1 = (y - half).clip(0, height - 1)
        y2 = (y + half).clip(0, height - 1)

        area = (y2 - y1 + 1) * (x2 - x1 + 1)

        sums = integral[y2 + 1, x2 + 1] - integral[y2 + 1, x1] - integral[y1, x2 + 1] + integral[y1, x1]
        means = sums / area

        sqr_sums = integral_sq[y2 + 1, x2 + 1] - integral_sq[y2 + 1, x1] - integral_sq[y1, x2 + 1] + integral_sq[y1, x1]
        stds = np.sqrt(sqr_sums / area - np.square(means))

        R = np.max(stds)
        M = np.min(image_gray)

        thresholds = ((1 - self.k) * means + self.k * M + self.k * stds / R * (means - M))

        result_image = np.zeros_like(image_gray, dtype=np.uint8)
        result_image[image_gray >= thresholds] = 255

        return result_image

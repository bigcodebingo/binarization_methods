import numpy as np
from src.models.ImageProcessor import ImageProcessor
from src.models.Binarizer import Binarizer

class Global(Binarizer):
    def __init__(self, thresh):
        self.thresh = thresh

    def threshold_otsu(self, hist):
        total_pixels = np.sum(hist)
        current_max, thresh = 0, 0
        sum_total = np.dot(np.arange(256), hist)
        sum_background, weight_background = 0, 0

        for i in range(256):
            weight_background += hist[i]
            weight_foreground = total_pixels - weight_background

            if weight_background == 0 or weight_foreground == 0:
                continue

            sum_background += i * hist[i]
            mean_background = sum_background / weight_background
            mean_foreground = (sum_total - sum_background) / weight_foreground

            between_class_variance = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2

            if between_class_variance > current_max:
                current_max = between_class_variance
                thresh = i

        return thresh

    def threshold(self, image):
        image_gray = ImageProcessor.to_gray(image)

        if self.thresh == 'otsu':
            hist_values, bins = np.histogram(image_gray, bins=256, range=(0, 256))
            thresh_value = self.threshold_otsu(hist_values)
        else:
            thresh_value = self.thresh

        height, width = ImageProcessor.get_size(image_gray)
        result_image = np.zeros_like(image_gray, dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                if image_gray[y, x] > thresh_value:
                    result_image[y, x] = 255

        return result_image

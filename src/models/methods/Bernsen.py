import numpy as np
from src.models.ImageProcessor import ImageProcessor
from src.models.Binarizer import Binarizer

class Bernsen(Binarizer):
    def __init__(self, window_size=15, contrast_threshold=15, gthresh=128):
        self.window_size = window_size
        self.contrast_threshold = contrast_threshold
        self.gthresh = gthresh

    def threshold(self, image):
        image_gray = ImageProcessor.to_gray(image)

        height, width = image_gray.shape
        padding = self.window_size // 2
        padded_image = np.pad(image_gray, pad_width=padding, mode='edge')

        result_image = np.zeros_like(image_gray, dtype=np.uint8)

        for y in range(padding, height + padding):
            for x in range(padding, width + padding):
                window = padded_image[y - padding:y + padding + 1, x - padding:x + padding + 1]

                i_max = np.max(window)
                i_min = np.min(window)

                i_mean = i_max / 2. + i_min / 2.

                if i_max - i_min < self.contrast_threshold:
                    result_image[y - padding, x - padding] = 255 if i_mean < self.gthresh else 0
                else:
                    result_image[y - padding, x - padding] = 255 if image_gray[y - padding, x - padding] < i_mean else 0

        return result_image

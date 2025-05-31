import numpy as np
from src.models.ImageProcessor import ImageProcessor
from src.models.methods.Global import Global
from src.models.Binarizer import Binarizer

class Eikwel(Binarizer):
    def __init__(self, r_size, R_size, count=0, eps=10):
        self.r_size = r_size
        self.R_size = R_size
        self.count = count
        self.eps = eps
        self.otsu = Global(thresh='otsu')

    def check_mean(self, array):
        return np.mean(array) if array.size > 0 else None

    def replace_block(self, image, start_x, start_y, flag):
        res = False
        to_black = False
        half_R = self.R_size // 2

        x_left_R = max(0, start_x - half_R)
        x_right_R = min(image.shape[1], start_x + half_R + self.r_size)
        y_left_R = max(0, start_y - half_R)
        y_right_R = min(image.shape[0], start_y + half_R + self.r_size)

        R_pixels = image[y_left_R:y_right_R, x_left_R:x_right_R].copy()
        gray_R_pixels = ImageProcessor.to_gray(R_pixels)

        hist_values, bins = np.histogram(gray_R_pixels, bins=256, range=(0, 256))
        otsu_threshold = self.otsu.threshold_otsu(hist_values)

        max_R_pixels = gray_R_pixels[gray_R_pixels >= otsu_threshold]
        min_R_pixels = gray_R_pixels[gray_R_pixels < otsu_threshold]

        mean_max_R_pixels = self.check_mean(max_R_pixels)
        mean_min_R_pixels = self.check_mean(min_R_pixels)
        mean_gray_R_pixels = self.check_mean(gray_R_pixels)

        if abs(0 - mean_gray_R_pixels) < abs(255 - mean_gray_R_pixels):
            to_black = True

        if mean_max_R_pixels is None or mean_min_R_pixels is None:
            res = True
        elif abs(mean_max_R_pixels - mean_min_R_pixels) > self.eps:
            res = True

        if not flag:
            x_left_r = start_x
            x_right_r = min(start_x + self.r_size, image.shape[1])
            y_left_r = start_y
            y_right_r = min(start_y + self.r_size, image.shape[0])
        else:
            x_right_r = start_x
            x_left_r = max(start_x - self.r_size, 0)
            y_left_r = start_y
            y_right_r = min(start_y + self.r_size, image.shape[0])

        r_pixels = image[y_left_r:y_right_r, x_left_r:x_right_r].copy()
        gray_r_pixels = ImageProcessor.to_gray(r_pixels)

        if res:
            binary_block = np.where(gray_r_pixels >= otsu_threshold, 255, 0).astype(np.uint8)
        elif to_black:
            gray_r_pixels[:] = 0
            binary_block = gray_r_pixels
        else:
            gray_r_pixels[:] = 255
            binary_block = gray_r_pixels

        if len(image.shape) == 3:
            image[y_left_r:y_right_r, x_left_r:x_right_r] = np.repeat(binary_block[:, :, np.newaxis], 3, axis=2)
        else:
            image[y_left_r:y_right_r, x_left_r:x_right_r] = binary_block

    def threshold(self, image):
        height, width = ImageProcessor.get_size(image)
        cur_count = 0
        reverse = False

        for start_y in range(0, height, self.r_size):
            if reverse:
                x_range = range(width, 0, -self.r_size)
            else:
                x_range = range(0, width, self.r_size)

            for start_x in x_range:
                self.replace_block(image, start_x, start_y, reverse)
                cur_count += 1
                if self.count != 0 and cur_count == self.count:
                    return image
            reverse = not reverse

        return image

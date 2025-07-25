import cv2
import numpy as np
from matplotlib import pyplot as plt

class ImageProcessor:

    @staticmethod
    def read_image(image_file, gray_scale=False):
        image_source = cv2.imread(image_file)
        if image_source is None: print("не удалось загрузить изображение"); return None

        if gray_scale:
            image_source = cv2.cvtColor(image_source, cv2.COLOR_BGR2GRAY)
        else:
            image_source = cv2.cvtColor(image_source, cv2.COLOR_BGR2RGB)

        return image_source

    @staticmethod
    def save_image(image, output_file):
        if image.ndim == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.imwrite(output_file, image)

    @staticmethod
    def show_by_plot(images, titles):
        for i, (image, title) in enumerate(zip(images, titles)):
            plt.subplot(1, len(images), i + 1)
            plt.imshow(image, cmap='gray' if image.ndim == 2 else None)
            plt.title(title)
            plt.axis('off')
        plt.show()

    @staticmethod
    def get_size(image):
        height, width = image.shape[:2]
        return [height, width]

    @staticmethod
    def to_gray(image):
        if len(image.shape) == 3:
            return np.round(0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]).astype(np.uint8)
        else:
            return image

    @staticmethod
    def hist(image):
        hist_values, bins = np.histogram(image, bins=256, range=(0, 256))
        # plt.bar(bins[:-1], hist_values, color='b', width=5, align='center', alpha=0.25)
        # plt.show()
        return hist_values
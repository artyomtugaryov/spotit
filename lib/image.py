import os
from typing import List, Optional

import cv2
import numpy as np
import imutils


class Image:
    def __init__(self, image: np.array, name: str = None, contours: List[np.ndarray] = None):
        """
        Uses path to image to process an image.

        :param image: Mat - image read using opencv
        :param name: str - name of the image
        """

        self.image = image
        self.name = name
        self.image_contours = contours or []

    @classmethod
    def read_from_path(cls, path_to_img: str):
        name = os.path.basename(path_to_img)
        cv_image = cv2.imread(path_to_img)
        return cls(image=cv_image, name=name)

    def add_contrast(self) -> 'Image':
        """
        Add contrast to an image
        """
        lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        l_chanel, a_chanel, b_chanel = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l_chanel)
        limg = cv2.merge((cl, a_chanel, b_chanel))
        result_image = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return self._new_image(result_image)

    def save_image(self, directory: str, file_name: str = None):
        """Save image in specified directory

        :param directory: str - directory to save the image
        :param file_name: str - name of file to save the image
        """
        file_name = file_name or self.name
        if not os.path.exists(directory):
            os.makedirs(directory)
        cv2.imwrite(os.path.join(directory, file_name), self.image)

    def resize_image(self, size=(800, 800)):
        """
        Resize image
        :param size: tuple - new size
        :return: Image resized to new size
        """
        return self._new_image(cv2.resize(self.image, size))

    def threshold(self, threshold: int = 190, bitwise_not: bool = False) -> 'Image':
        threshed_image = cv2.threshold(self.image, threshold, 255, cv2.THRESH_BINARY)[1]
        if bitwise_not:
            threshed_image = cv2.bitwise_not(threshed_image)
        return self._new_image(threshed_image)

    def gray(self) -> 'Image':
        return self._new_image(cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY))

    def contours(self):
        contours = cv2.findContours(self.image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return sorted(imutils.grab_contours(contours), key=cv2.contourArea, reverse=True)

    def keep_contour(self, contour, mask_value: int = 255) -> 'Image':
        """
        Get Image with content of the contour and mask_value background
        :param contour: contour to keep on image
        :param mask_value: int - value of background color
        :return: Image with content of contour on [mask_value]*3 background
        """
        white_color = [mask_value] * 3
        stencil = np.zeros(self.image.shape[:-1]).astype(np.uint8)
        cv2.fillPoly(stencil, [contour], mask_value)
        result = self.image.copy()
        result[stencil != mask_value] = white_color
        return self._new_image(result)

    @staticmethod
    def get_rect_coordinates_around_contour(contour):
        return cv2.boundingRect(contour)

    @staticmethod
    def bounding_square_around_contour(contour):
        x, y, w, h = Image.get_rect_coordinates_around_contour(contour)
        # create squares io rects
        if w < h:
            x += int((w - h) / 2)
            w = h
        else:
            y += int((h - w) / 2)
            h = w
        return x, y, w, h

    def take_out_roi(self, x, y, w, h):
        return self._new_image(self.image[y:y + h, x:x + w])

    def copy(self) -> 'Image':
        return self._new_image(self.image)

    def _new_image(self, image_content: np.array) -> 'Image':
        return Image(image=image_content, name=self.name, contours=self.image_contours)

    def add_contour(self, contour, color):
        cv2.drawContours(self.image, [contour], -1, color, 3)
        self.image_contours.append(contour)

    def draw_contour(self, contour, color=(0, 255, 0)) -> 'Image':
        new_image = self.copy()
        new_image.add_contour(contour=contour, color=color)
        self.image_contours = new_image.image_contours
        return new_image

    @property
    def height(self) -> int:
        return self.image.shape[0]

    @property
    def width(self) -> int:
        return self.image.shape[1]

    @property
    def id(self) -> int:
        image_name, _  = os.path.splitext(self.name)
        image_id = image_name.split('_')[-1]
        return int(image_id)

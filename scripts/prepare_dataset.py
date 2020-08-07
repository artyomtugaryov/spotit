import os

import cv2

from lib.image import Image
from lib.constants import SOURCE_IMAGES_PATH, PROCESSED_IMAGES_PATH, ICONS_PATH
from lib.utils import list_files_in_dir

if __name__ == '__main__':
    images_paths = list_files_in_dir(SOURCE_IMAGES_PATH)

    for image_path in images_paths:
        # Read an image with a card
        image = Image.read_from_path(path_to_img=os.path.join(SOURCE_IMAGES_PATH, image_path))
        # Preprocess image to get contours
        resized_image = image.add_contrast().resize_image()
        preprocessed_image = resized_image.gray().threshold()
        # Find contours in the image
        contours = preprocessed_image.contours()
        largest_contour = contours[0]
        # Get image with card only in withe background
        card_image = resized_image.keep_contour(largest_contour)
        x, y, w, h = Image.bounding_square_around_contour(contours[0])
        processed_card = card_image.take_out_roi(x, y, w, h)
        processed_card.save_image(PROCESSED_IMAGES_PATH)

        icons_contours = processed_card.gray().threshold(bitwise_not=True).contours()
        for index, contour in enumerate(icons_contours):
            if cv2.contourArea(contour) < 1000:
                continue
            icon_image = processed_card.keep_contour(contour)
            x, y, w, h = Image.bounding_square_around_contour(contour)
            processed_icon = icon_image.take_out_roi(x, y, w, h)
            icon_name = os.path.splitext(icon_image.name)[0]
            processed_icon.save_image(ICONS_PATH, f'{icon_name}_{index}.jpeg')

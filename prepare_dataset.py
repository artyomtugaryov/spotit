import os

import cv2

from lib.image import Image
from constants import SOURCE_IMAGES_PATH, PROCESSED_IMAGES_PATH, ICONS_PATH
from lib.utils import list_files_in_dir

if __name__ == '__main__':
    images_paths = list_files_in_dir(SOURCE_IMAGES_PATH)

    for image_path in images_paths:
        image = Image.read_from_path(path_to_img=os.path.join(SOURCE_IMAGES_PATH, image_path))
        contrasted_image = image.add_contrast()
        resized_image = contrasted_image.resize_image()
        contours = resized_image.gray().threshold().contours()
        output = resized_image.keep_contour_with_white_background(contours[0])
        x, y, w, h = Image.bounding_square_around_contour(contours[0])
        processed_card = output.take_out_roi(x, y, w, h)
        processed_card.save_image(PROCESSED_IMAGES_PATH)

        icons_contours = processed_card.gray().threshold(bitwise_not=True).contours()
        for index, contour in enumerate(icons_contours):
            if cv2.contourArea(contour) < 1000:
                continue
            x, y, w, h = Image.bounding_square_around_contour(contour)
            processed_icon = processed_card.take_out_roi(x, y, w, h)
            icon_name = os.path.splitext(processed_card.name)[0]
            processed_icon.save_image(ICONS_PATH, f'{icon_name}_{index}.jpeg')

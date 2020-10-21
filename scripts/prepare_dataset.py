import argparse
import os

import cv2

from lib.constants import ICONS_PATH
from lib.datasets_adapter.coco import COCOAdapter
from lib.image import Image
from lib.utils import list_files_in_dir

SAVE_ICONS = os.getenv('SAVE_ICONS', False)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-images-path', '-s',
                        required=True,
                        type=str)
    parser.add_argument('--output-images-path', '-o',
                        required=True,
                        type=str)
    parser.add_argument('--save-icons',
                        action='store_true')
    return parser.parse_args()


if __name__ == '__main__':

    args = parse_arguments()

    images_paths = list_files_in_dir(args.source_images_path)
    images = []
    for image_path in images_paths:
        # Read an image with a card
        image = Image.read_from_path(path_to_img=os.path.join(args.source_images_path, image_path))
        # Preprocess image to get contours
        contrasted_image = image.add_contrast()
        preprocessed_image = contrasted_image.gray().threshold()
        # Find contours in the image
        contours = preprocessed_image.contours()
        largest_contour = contours[0]
        # Get image with card only in withe background
        card_image = contrasted_image.keep_contour(largest_contour)
        x, y, w, h = Image.bounding_square_around_contour(contours[0])
        processed_card = card_image.take_out_roi(x, y, w, h)
        try:
            processed_card.save_image(args.output_images_path)
        except Exception as e:
            print(f'Cannot save processed image {image_path}')
            print(e)
            continue
        images.append(processed_card)
        icons_contours = processed_card.gray().threshold(bitwise_not=True).contours()
        for index, contour in enumerate(icons_contours):
            if cv2.contourArea(contour) < 1000:
                continue
            processed_card.draw_contour(contour)
            if not args.save_icons:
                continue
            icon_image = processed_card.keep_contour(contour)
            x, y, w, h = Image.bounding_square_around_contour(contour)
            processed_icon = icon_image.take_out_roi(x, y, w, h)
            icon_name = os.path.splitext(icon_image.name)[0]
            icon_path = os.path.join(args.output_images_path, ICONS_PATH)
            processed_icon.save_image(icon_path, f'{icon_name}_{index}.jpeg')
        print(f'Successfully processed {image_path}')
    COCOAdapter(images).save_annotations(args.output_images_path)

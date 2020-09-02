import json
from typing import List, Dict

import cv2

from lib.datasets_adapter.datase_adapter import DatasetAdapter
from lib.image import Image


class COCOAdapter(DatasetAdapter):
    def get_categories(self) -> list:
        labels = [
            'hammer', 'lightning', 'fire', 'ghost', 'key', 'cat', 'icecube', 'snowflake',
            'turtle', 'milkbottle', 'eye', 'clown', 'cactus', 'gkey', 'cobweb', 'lightbulb',
            'carrot', 'hand', 'bird', 'stopsign', 'igloo', 'lips', 'flower', 'exclamationmark',
            'car', 'lock', 'anchor', 'moon', 'man', 'clock', 'tree', 'heart', 'spider', 'stains',
            'dolphin', 'apple', 'ladybug', 'trex', 'sun', 'cheese', 'questionmark', 'dog', 'horse',
            'flyingdino', 'zebra', 'yinyang', 'sunglasses', 'skull', 'candle', 'snowman', 'leaf',
            'drop', 'bomb', 'scissors', 'pencil', 'bullseye', 'clover'
        ]
        categories = [
            {
                'id': 1,
                'name': 'icon',
                "supercategory": "icon"
            },
        ]
        for index, label in enumerate(labels, start=len(categories) +1):
            categories.append(
                {
                    'id': index,
                    'name': label,
                    'supercategory': 'icon'
                }
            )
        return categories

    def save_annotations(self, annotations_file_path: str):
        images = []
        annotations = []
        result = {
            'images': images,
            'annotations': annotations,
            'categories': self.get_categories(),
            "licenses": [
                {
                    "id": 1,
                    "name": "Attribution-NonCommercial-ShareAlike License",
                    "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
                },
            ],
            'info': {
                "contributor": "Artyom Tugaryov",
                "date_created": "2020/09/01",
                "description": "Spot It like  COCO 2017 dataset ",
                "url": "http://null",
                "version": "1.0",
                "year": 2020
            }
        }

        for image in self.images:
            images.append(self.get_image_data(image))
            annotations.extend(self.get_annotation_data(image))
        with open(annotations_file_path, 'w') as annotation_file:
            json.dump(result, annotation_file)

    @staticmethod
    def get_image_data(image: Image) -> dict:
        return {
            "coco_url": "http://images.cocodataset.org/val2017/000000474028.jpg",
            "date_captured": "2013-11-20 22:40:01",
            "flickr_url": "http://farm8.staticflickr.com/7086/7258228366_b29766be26_z.jpg",
            'file_name': image.name,
            'height': image.height,
            'width': image.width,
            'id': image.id,
            'license': 1
        }

    @staticmethod
    def get_annotation_data(image: Image) -> List[Dict]:
        results = []
        for index, contour in enumerate(image.image_contours):
            results.append(
                {
                    # Only ONE category! You need set a real category manually
                    'category_id': 1,
                    'image_id': image.id,
                    'id': int(f'{image.id}{index}'),
                    'iscrowd': 0,
                    'segmentation': [COCOAdapter.get_segmentation_annotations(contour)],
                    'area': cv2.contourArea(contour),
                    'bbox': COCOAdapter.get_bbox_annotations(contour)
                }
            )
        return results

    @staticmethod
    def get_segmentation_annotations(contour) -> List[int]:
        contour_points = []
        for point in contour:
            point = point[0]
            contour_points.extend(tuple(map(float, point)))
        return contour_points

    @staticmethod
    def get_bbox_annotations(contour) -> List[List[int]]:
        bbox = cv2.boundingRect(contour)
        return bbox

from typing import List

from lib.image import Image


class DatasetAdapter:
    def __init__(self, images: List[Image]):
        self.images = images

    def save_annotations(self, path: str):
        raise NotImplementedError

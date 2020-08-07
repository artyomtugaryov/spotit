import os

DATA_PATH = os.getenv('DATA_PATH', os.path.join(os.curdir, 'data'))
SOURCE_IMAGES_PATH = os.path.join(DATA_PATH, 'source_images')
PROCESSED_IMAGES_PATH = os.path.join(DATA_PATH, 'processed_images')
ICONS_PATH = os.path.join(DATA_PATH, 'icons')

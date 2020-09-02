import os

ROOT_DIR = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.getenv('DATA_PATH', os.path.join(ROOT_DIR, 'data'))
SOURCE_IMAGES_PATH = os.getenv('SOURCE_IMAGES_PATH', os.path.join(DATA_PATH, 'source_images'))
PROCESSED_IMAGES_PATH = os.getenv('PROCESSED_IMAGES_PATH', os.path.join(DATA_PATH, 'processed_images'))
ICONS_PATH = os.path.join(DATA_PATH, 'icons')

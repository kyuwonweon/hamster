from enum import Enum, auto
import cv2
import os


class State(Enum):
    PEACE = auto()
    THUMBS_UP = auto()
    TWO_HANDS_APART = auto()
    TWO_HANDS_TOGETHER = auto()
    ONE_HAND = auto()
    SHUFFLING = auto()


IMAGE_PATHS = {
    State.PEACE: 'images/v.png',
    State.THUMBS_UP: 'images/thumbsup.jpg',
    State.TWO_HANDS_APART: 'images/twohand.jpg',
    State.TWO_HANDS_TOGETHER: 'images/together.jpg',
    State.ONE_HAND: 'images/onehand.jpg'
}

images = {}

for state, path in IMAGE_PATHS.items():
    if os.path.exists(path):
        img = cv2.imread(path)
        img = cv2.resize(img, (500, 500))
        images[state] = img
    else:
        print(f"Could not find '{path}'.")

image_list = list(images.values())

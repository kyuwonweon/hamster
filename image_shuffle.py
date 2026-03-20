import cv2
import os
import random

image_filenames = [
    'images/thumbsup.jpg',
    'images/v.jpg',
    'images/onehand.jpg',
    'images/twohand.jpg',
    'images/together.jpg'
]
images = []

# load and resize images
for filename in image_filenames:
    if os.path.exists(filename):
        img = cv2.imread(filename)
        img = cv2.resize(img, (500, 500))
        images.append(img)
    else:
        print(f"Could not find '{filename}'.")
if not images:
    print("Exiting due to no image loaded.")
    exit()

# Shuffle
idx = 0
while True:
    cv2.imshow('Hamster Images', images[idx])
    idx = random.randint(0, len(images) - 1)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cv2. destroyAllWindows()

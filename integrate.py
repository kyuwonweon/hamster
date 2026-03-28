from enum import Enum, auto
import cv2
import os
import math
import mediapipe as mp
import random


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
if not image_list:
    print("No images loaded.")
    exit()


def detect_gesture(handmarks):
    num_hands = len(handmarks)
    if num_hands == 0:
        return State.SHUFFLING
    elif num_hands == 2:
        wrist1 = handmarks[0].landmark[0]
        wrist2 = handmarks[1].landmark[0]
        distance = math.hypot(wrist1.x - wrist2.x, wrist1.y, wrist2.y)

        if distance < 0.2:
            return State.TWO_HANDS_TOGETHER
        else:
            return State.TWO_HANDS_APART

    # one hand landmark
    lm = handmarks[0].landmark
    thumb_up = lm[4].y < lm[3].y
    index_up = lm[8].y < lm[6].y
    middle_up = lm[12].y < lm[10].y
    ring_up = lm[16].y < lm[14].y
    pinky_up = lm[20].y < lm[18].y

    if index_up and middle_up and not ring_up and not pinky_up:
        return State.PEACE
    elif index_up and middle_up and ring_up and pinky_up:
        return State.ONE_HAND
    elif thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
        return State.THUMBS_UP
    return State.SHUFFLING


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=2 
)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignore empty camera frame")
        continue
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    current_state = State.SHUFFLING

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        current_state = detect_gesture(results.multi_hand_landmarks)

    if current_state == State.SHUFFLING:
        display_img = random.choice(image_list)
    else:
        display_img = images[current_state]

    cv2.imshow('Hamster Roulette', display_img)
    cv2.imshow('Pose for Hamsters', frame)

    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


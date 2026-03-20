import cv2
import mediapipe as mp

# Setup MediaPipe for hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.7
    )
# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ingore empty camera frame")
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convert BGR to RGB
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow('Pose for Hamsters', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp

# Initialize webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ingore empty camera frame")
        continue

    cv2.imshow('Hamsters', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

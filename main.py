import cv2
import numpy as np
import subprocess

screen_width = 600
screen_height = 800
b1_x = 200
b1_y = 250
b2_x = 200
b2_y = 350
b_w = 340
b_h = 80
bg_color = (240, 230, 220)
hover_color = (150, 120, 255)
button_color = (200, 180, 255)
shadow_color = (200, 200, 200)
text_color = (255, 255, 255)
mouse_x = 0
mouse_y = 0
user_choice = None


def mouse_events(event, x, y, flags, param):
    global mouse_x, mouse_y, user_choice
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y
    elif event == cv2.EVENT_LBUTTONDOWN:
        if b1_x <= x <= b1_x + b_w and b1_y <= y <= b1_y + b_h:
            user_choice = "MATCH"
        elif b2_x <= x <= b2_x + b_w and b2_y <= y <= b2_y + b_h:
            user_choice = "GRAB"


def create_button(img, txt, x, y, w, h, hover):
    color = hover_color if hover else button_color
    r = h//2

    # Create shadow
    cv2.circle(img, (x + r + 4, y + r + 4), r, shadow_color, -1)
    cv2.circle(img, (x + w - r + 4, y + r + 4), r, shadow_color, -1)
    cv2.rectangle(img, (x + r + 4, y + 4), (x + w - r + 4, y + h + 4),
                  shadow_color, -1)

    # Create button
    cv2.circle(img, (x + r, y + r), r, color, -1)
    cv2.circle(img, (x + w - r, y + r), r, color, -1)
    cv2.rectangle(img, (x + r, y), (x + w - r, y + h), color, -1)

    # Add text
    font = cv2.FONT_HERSHEY_DUPLEX
    text_size = cv2.getTextSize(txt, font, 0.9, 2)[0]
    text_x = x + (w - text_size[0]) // 2
    text_y = y + (h + text_size[1]) // 2

    cv2.putText(img, txt, (text_x, text_y), font, 0.9, text_color, 2)


cv2.namedWindow('Hamster Game')
cv2.setMouseCallback('Hamster Game', mouse_events)

while True:
    screen = np.zeros((screen_width, screen_height, 3), dtype=np.uint8)
    screen[:] = bg_color
    cv2.putText(screen, "CHOOSE YOUR GAME!", (150, 200), cv2.FONT_HERSHEY_DUPLEX,
                1.5, (0, 0, 0), 3)
    hover1 = (b1_x <= mouse_x <= b1_x + b_w and b1_y <= mouse_y <= b1_y+b_h)
    hover2 = (b2_x <= mouse_x <= b2_x + b_w and b2_y <= mouse_y <= b2_y+b_h)
    create_button(screen, "Pose-a-Hamster", b1_x, b1_y, b_w, b_h, hover1)
    create_button(screen, "Grab-a-Hamster", b2_x, b2_y, b_w, b_h, hover2)
    cv2.imshow("Hamster Game", screen)

    if user_choice == "MATCH":
        print("Launching Pose-a-Hamster...")
        cv2.destroyAllWindows()
        subprocess.run(["python3", "integrate.py"])
        break
    elif user_choice == "GRAB":
        print("Launching Pinch & Catch...")
        cv2.destroyAllWindows()
        break

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destryAllWindows()

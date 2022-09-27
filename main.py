import cv2
import autopy
import mediapipe as mp
# import time
# import math
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)
width, height = autopy.screen.size()
hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1,
                                 min_tracking_confidence=0.5, min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

while True:
    _, img = cap.read()
    result = hands.process(img)
    #print(result)
    if result.multi_hand_landmarks:
        enum = enumerate(result.multi_hand_landmarks[0].landmark)

        for id, lm in enum:
            h, w, _ = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 3, (255, 0, 255))
            if id == 8:

                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                try:
                    autopy.mouse.move(width-cx * width / w, cy * height / h)
                except ValueError:
                    continue
        mpDraw.draw_landmarks(img, result.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', cv2.flip(img, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

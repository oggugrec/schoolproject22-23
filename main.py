import cv2
import autopy
import mediapipe as mp
import pyautogui as gui

cap = cv2.VideoCapture(0)
width, height = autopy.screen.size()
hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1,
                                 min_tracking_confidence=0.5, min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

flag_mouse_tracking = False
tipIds = [4, 8, 12, 16, 20]


def finger_position(image, hand_no=0):
    lm_list = []
    if result.multi_hand_landmarks:
        my_hand = result.multi_hand_landmarks[hand_no]
        for id, lm in enumerate(my_hand.landmark):
            # print(id,lm)
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append([id, cx, cy])
    return lm_list


while True:

    _, img = cap.read()
    result = hands.process(img)
    if result.multi_hand_landmarks:
        enum = enumerate(result.multi_hand_landmarks[0].landmark)
        for id, lm in enum:
            h, w, _ = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 3, (255, 0, 255))
            lmList = finger_position(img)
            fingers = []
            if len(lmList) != 0:
                for finger_id in range(1, 5):
                    if lmList[tipIds[finger_id]][2] < lmList[tipIds[finger_id] - 2][2]:
                        fingers.append(1)
                    if lmList[tipIds[finger_id]][2] > lmList[tipIds[finger_id] - 2][2]:
                        fingers.append(0)
                total_fingers = fingers.count(1)

            try:
                if id == 8 and fingers[0] == fingers[1] == 1 and fingers[2] == fingers[3] == 0:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    try:
                        gui.moveTo(width - cx * width / w, cy * height / h)
                    except ValueError:
                        continue
            except IndexError:
                continue

            try:
                if fingers[0] == 1 and fingers[1] == fingers[2] == fingers[3] == 0:
                    gui.click()
            except IndexError:
                continue
        mpDraw.draw_landmarks(img, result.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', cv2.flip(img, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

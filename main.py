import cv2
import autopy
import mediapipe as mp
import pyautogui as gui
from pynput.keyboard import Key, Controller
import time


cap = cv2.VideoCapture(0)
width, height = autopy.screen.size()
hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, model_complexity=1,
                                 min_tracking_confidence=0.5, min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
keyboard = Controller()

flag_mouse_tracking = False
tipIds = [4, 8, 12, 16, 20]
lmb_timer, rmb_timer = 0, 0
previous_volume = 100


def finger_position(image, hand_no=0):
    lm_list = []
    if result.multi_hand_landmarks:
        my_hand = result.multi_hand_landmarks[hand_no]
        for id, lm in enumerate(my_hand.landmark):
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
                volume = lmList[9][2]
                total_fingers = fingers.count(1)
            # mouse moving
            # курсор следует за указательным пальцем, остальные пальцы прижаты
            try:
                if id == 8 and ((fingers[0] == 1 and fingers[1] == fingers[2] == fingers[3] == 0) or fingers[0] == 0 and
                                fingers[1] == fingers[2] == fingers[3] == 1):
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    try:
                        gui.moveTo(width - cx * width / w, cy * height / h)
                    except ValueError:
                        continue
            except IndexError:
                continue
            # lmb click
            # отслеживается по раскрытым указательному и среднему пальцам, остальные прижаты
            try:
                if ((fingers[0] == fingers[1] == 1 and fingers[2] == fingers[3] == 0) or
                        (fingers[0] == fingers[1] == 0 and fingers[2] == fingers[3] == 1)):
                    if lmb_timer == 0 or time.time() - lmb_timer > 1:
                        gui.click()
                        lmb_timer = time.time()
                    elif time.time() - lmb_timer > 2:
                        lmb_timer = 0
            except IndexError or gui.FailSafeException:
                continue
            # rmb click
            # отслеживается по раскрытым указательному, среднему и безымянному пальцам, остальные прижаты
            try:
                if (fingers[0] == fingers[1] == fingers[2] == 1 and fingers[3] == 0) or\
                        (fingers[0] == fingers[1] == fingers[2] == 0 and fingers[3] == 1):
                    if rmb_timer == 0 or time.time() - rmb_timer > 1:
                        gui.click(button='Right')
                        rmb_timer = time.time()
                    elif time.time() - rmb_timer > 2:
                        rmb_timer = 0
            except IndexError or gui.FailSafeException:
                continue
            # volume changing
            # все пальцы раскрыты, большой и мизинец расставлены широко, остальные прижаты друг к другу
            if abs(lmList[4][1] - lmList[5][1]) > 50 and abs(lmList[20][1] - lmList[15][1]) > 30 and\
                    fingers[0] == fingers[1] == fingers[2] == 1 and abs(lmList[8][1] - lmList[16][1]) < 75:
                if volume < previous_volume:
                    keyboard.press(Key.media_volume_up)
                    keyboard.release(Key.media_volume_up)
                elif volume > previous_volume:
                    keyboard.press(Key.media_volume_down)
                    keyboard.release(Key.media_volume_down)
                previous_volume = volume
        mpDraw.draw_landmarks(img, result.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)
    cv2.imshow('Controller', cv2.flip(img, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


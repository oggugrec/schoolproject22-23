import cv2
import autopy
import mediapipe as mp


cap = cv2.VideoCapture(0)
width, height = autopy.screen.size()
hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1,
                                 min_tracking_confidence=0.5, min_detection_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

flag_mouse_tracking = False
tipIds = [4, 8, 12, 16, 20]


def fingerPosition(image, handNo=0):
    lmList = []
    if result.multi_hand_landmarks:
        myHand = result.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            # print(id,lm)
            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    return lmList


while True:

    _, img = cap.read()
    result = hands.process(img)
    # print(result)

    if result.multi_hand_landmarks:
        enum = enumerate(result.multi_hand_landmarks[0].landmark)
        for id, lm in enum:
            h, w, _ = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 3, (255, 0, 255))
            if id == 8:
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                if flag_mouse_tracking:
                    try:
                        autopy.mouse.move(width - cx * width / w, cy * height / h)
                    except ValueError:
                        continue
                    lmList = fingerPosition(img)
                    if len(lmList) != 0:
                        fingers = []
                        for id in range(1, 5):
                            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                                fingers.append(1)
                            if lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2]:
                                fingers.append(0)
                        total_fingers = fingers.count(1)
                        if total_fingers == 0 and flag_mouse_tracking:
                            flag_mouse_tracking = False
                else:
                    lmList = fingerPosition(img)
                    if len(lmList) != 0:
                        fingers = []
                        for id in range(1, 5):
                            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                                fingers.append(1)
                            if lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2]:
                                fingers.append(0)
                        total_fingers = fingers.count(1)
                        if total_fingers == 0:
                            flag_mouse_tracking = True
        mpDraw.draw_landmarks(img, result.multi_hand_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', cv2.flip(img, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

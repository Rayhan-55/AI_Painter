import cv2 as cv
import os
import numpy as np
import mediapipe as mp

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils

tipIds = [4, 8, 12, 16, 20]
brushthiness = 15
eraserthickness = 50
xp, yp = 0, 0
drawcolor = (0, 255, 0)


imgcanvas = np.zeros((1080, 1920, 3), np.uint8)


folderPath = "Photos"
myList = os.listdir(folderPath)
overlay = []

for impath in myList:
    img = cv.imread(f"{folderPath}/{impath}")
    if img is not None:
        overlay.append(img)

design = overlay[0]


def resize_aspect(img, width=None, height=None):
    h, w = img.shape[:2]
    if width is not None:
        scale = width / w
        return cv.resize(img, (width, int(h * scale)))
    else:
        scale = height / h
        return cv.resize(img, (int(w * scale), height))


cap = cv.VideoCapture(1)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

success, img = cap.read()
if not success:
    print("Camera error")
    exit()

frame_h, frame_w = img.shape[:2]


design = resize_aspect(design, width=frame_w)
num_icons = len(overlay)


while True:
    success, img = cap.read()
    if not success:
        break

    img = cv.flip(img, 1)
    lmlist = []

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])

            mpDraw.draw_landmarks(img, hand, mphands.HAND_CONNECTIONS)

            if len(lmlist) != 0:
                x1, y1 = lmlist[8][1:]
                x2, y2 = lmlist[12][1:]

                fingers = []

                if lmlist[4][1] > lmlist[3][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                for i in range(1, 5):
                    if lmlist[tipIds[i]][2] < lmlist[tipIds[i] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)


                if fingers[1] and fingers[2]:
                    xp, yp = 0, 0
                    cv.rectangle(img, (x1, y1 - 25), (x2, y2 + 25),
                                 (0, 255, 0), cv.FILLED)

                    if y1 < design.shape[0]:
                        icon_width = design.shape[1] // num_icons
                        index = x1 // icon_width

                        if 0 <= index < num_icons:
                            design = resize_aspect(
                                overlay[index], width=frame_w
                            ).copy()

                            if index == 0:
                                drawcolor = (0, 255, 0)
                            elif index == 1:
                                drawcolor = (255, 0, 0)
                            elif index == 2:
                                drawcolor = (255, 0, 255)
                            elif index == 3:
                                drawcolor = (0, 0, 0)


                if fingers[1] and not fingers[2]:
                    cv.circle(img, (x1, y1), 15, drawcolor, cv.FILLED)

                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    thickness = eraserthickness if drawcolor == (0, 0, 0) else brushthiness

                    cv.line(img, (xp, yp), (x1, y1), drawcolor, thickness)
                    cv.line(imgcanvas, (xp, yp), (x1, y1), drawcolor, thickness)

                    xp, yp = x1, y1

    imgcanvas = cv.resize(imgcanvas, (img.shape[1], img.shape[0]))

    imggray = cv.cvtColor(imgcanvas, cv.COLOR_BGR2GRAY)
    _, imginv = cv.threshold(imggray, 50, 255, cv.THRESH_BINARY_INV)
    imginv = cv.cvtColor(imginv, cv.COLOR_GRAY2BGR)

    img = cv.bitwise_and(img, imginv)
    img = cv.bitwise_or(img, imgcanvas)


    dh, dw = design.shape[:2]
    img[0:dh, 0:dw] = design

    cv.imshow("Virtual Painter 1080p", img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

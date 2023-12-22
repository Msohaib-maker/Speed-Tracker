import random
import cv2
from tracker2 import *
import numpy as np

desired_width = 960
desired_height = 540
TerminationFlag = False

kernelOp = np.ones((3, 3), np.uint8)
kernelOp2 = np.ones((5, 5), np.uint8)
kernelCl = np.ones((11, 11), np.uint8)
kernel_e = np.ones((5, 5), np.uint8)


def PreProcessingFrame(frame):
    frame = cv2.resize(frame, (desired_width, desired_height))

    # converting frame into gray scale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Using Gaussian blurring to remove high freq noise
    gray_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)

    # Apply Fast Non-Local Means Denoising
    gray_frame = cv2.fastNlMeansDenoising(gray_frame, None, h=10, templateWindowSize=7, searchWindowSize=21)

    return gray_frame


def Perform_Contouring(img3, frame):
    detects = []
    contours, _ = cv2.findContours(img3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            detects.append([x, y, w, h])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return frame, detects


def Speed_Tracker():

    global TerminationFlag
    capture = cv2.VideoCapture('Car_motion4.mp4')
    fps = capture.get(cv2.CAP_PROP_FPS)
    # ret, img = capture.read()
    # img = PreProcessingFrame(img)

    object_detector = cv2.createBackgroundSubtractorMOG2(history=None, varThreshold=None, detectShadows=False)

    tracker = EuclideanDistTracker()

    while True:
        ret1, img1 = capture.read()

        if TerminationFlag:
            break

        if not ret1:
            break

        # Visual Frame
        roi = img1
        roi = cv2.resize(roi, (desired_width, desired_height))
        roi = roi[200:540, 0:400]

        # Extracting mask from the Frame
        diff = object_detector.apply(img1)
        ret, diff = cv2.threshold(diff, 254, 255, cv2.THRESH_BINARY)
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernelOp)
        diff = cv2.morphologyEx(diff, cv2.MORPH_CLOSE, kernelCl)
        diff = cv2.erode(diff, kernel_e)

        # Resizing the mask
        diff = cv2.resize(diff, (desired_width, desired_height))
        diff = diff[200:540, 0:400]

        # 1. Object detection
        c2, detections = Perform_Contouring(diff, roi)

        # 2. Object Tracking
        boxes_ids = tracker.update(detections)

        # 3. Mark tracked objects
        for box_id in boxes_ids:
            x, y, w, h, Id = box_id

            if tracker.getsp(Id) < tracker.limit():
                cv2.putText(roi, str(Id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1,
                            (0, 255, 255), 2)
                cv2.putText(roi, f"{str(tracker.getsp(Id))}km/h", (x + 40, y - 15), cv2.FONT_HERSHEY_PLAIN, 0.8,
                            (0, 255, 255), 2)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
            else:
                cv2.putText(roi, str(Id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 1,
                            (0, 0, 255), 2)
                cv2.putText(roi, f"{str(tracker.getsp(Id))}km/h", (x + 40, y - 15), cv2.FONT_HERSHEY_PLAIN, 0.8,
                            (0, 0, 255), 2)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 165, 255), 3)

            s = tracker.getsp(Id)
            if tracker.f[Id] == 1 and s != 0:
                tracker.capture(roi, x, y, h, w, s, Id)

        # DRAW LINES
        cv2.line(roi, (0, 80), (400, 80), (255, 0, 255), 1)
        cv2.line(roi, (0, 90), (400, 90), (255, 0, 255), 1)
        cv2.line(roi, (0, 180), (400, 180), (0, 0, 255), 1)
        cv2.line(roi, (0, 190), (400, 190), (0, 0, 255), 1)

        # Last. Display Objects
        cv2.imshow("Diff 1", diff)
        cv2.imshow("Frame", c2)

        img = img1
        c1 = c2

        key = cv2.waitKey(30)
        if key == 27:
            break

    cv2.destroyAllWindows()



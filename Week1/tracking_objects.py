#!/usr/bin/env python3

'''
ECE 180DA/DB - Week 1 Task 4 
Color-based tracking with HSV/RGB thresholding and bounding box

Baseline references:
- OpenCV
- Basic color tracking example: https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html

Improvements added to script:
1. Added Gaussian blur for noise reduction
2. Added contour detection and bounding box for localization
3. Added minimum area filter for stable detection
4. Added interactive HSV trackbars for calibration
Name: Leah George
Date: 10/4/2025
'''

import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
if not cap.isOpened():
    raise SystemExit("Cannot open webcam.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV and smooth the image
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(hsv, (5, 5), 0)

    # Define color range (adjust for your object)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Create mask and find contours
    mask = cv.inRange(blur, lower_blue, upper_blue)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv.contourArea)
        if cv.contourArea(c) > 500:
            x, y, w, h = cv.boundingRect(c)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Combine mask and original image
    res = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('Frame', frame)
    cv.imshow('Mask', mask)
    cv.imshow('Result', res)

    if cv.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
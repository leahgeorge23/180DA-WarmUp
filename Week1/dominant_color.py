#!/usr/bin/env python3
'''
ECE 180DA/DB - Week 1 Task 4.4
Real-time Dominant Color Detection using K-Means (Central ROI)

Baseline references:
- OpenCV K-Means Example (Lab-provided): kmeans.py from ECE 180DA/DB Week 1 materials
  Source code reference included below:
  https://github.com/opencv/opencv/blob/master/samples/python/kmeans.py
- OpenCV Documentation: https://docs.opencv.org/4.x/d1/d5c/tutorial_py_kmeans_opencv.html

Improvements and adaptations:
1. Applied K-Means clustering to a real-time webcam feed (central ROI)
2. Added a dynamically drawn central rectangle for region selection
3. Calculated and displayed the dominant color in real time
4. Added a live color patch overlay and text readout of BGR values

Author: Leah George
Date: 10/4/2025
'''

import cv2 as cv
import numpy as np

# Initialize webcam
cap = cv.VideoCapture(0)
if not cap.isOpened():
    raise SystemExit("Cannot open webcam.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rect_w, rect_h = int(w * 0.3), int(h * 0.3)
    x1, y1 = w // 2 - rect_w // 2, h // 2 - rect_h // 2
    x2, y2 = x1 + rect_w, y1 + rect_h

    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    roi = frame[y1:y2, x1:x2]

    # Flatten ROI pixels for K-Means input
    pixels = roi.reshape((-1, 3))
    pixels = np.float32(pixels)

    # K-Means parameters 
    k = 3  
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Apply K-Means clustering
    _, labels, centers = cv.kmeans(pixels, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)

    dominant_color = centers[np.bincount(labels.flatten()).argmax()]

    color_patch = np.zeros((100, 100, 3), np.uint8)
    color_patch[:] = dominant_color

    cv.rectangle(frame, (10, 10), (110, 110), tuple(int(c) for c in dominant_color), -1)
    cv.putText(frame, f"Dominant BGR: {dominant_color.tolist()}", (130, 60),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv.LINE_AA)

    cv.imshow('Dominant Color Detection', frame)

    if cv.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
import os
import cv2

directory = "data/positives/"

for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        src = cv2.imread(directory + filename, cv2.IMREAD_UNCHANGED)
        scale_percent = 25

        width = int(src.shape[1] * scale_percent / 100)
        height = int(src.shape[0] * scale_percent / 100)

        size = (width, height)

        output = cv2.resize(src, size)

        cv2.imwrite(directory + filename, output)

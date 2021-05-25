import numpy as np
import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)
def Test():

    while(True):
        ret, img = cap.read()

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([60, 40, 40])
        upper_blue = np.array([100, 255, 255])

        maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)

        resBlue = cv2.bitwise_and(img, img, mask=maskBlue)

        gray = cv2.cvtColor(resBlue, cv2.COLOR_BGR2GRAY)

        stop_data = cv2.CascadeClassifier('cascade/cascade.xml')
        print("HEre")
        found = stop_data.detectMultiScale(gray,
                                           minSize=(100, 100))
        print("Now Here")
        # Don't do anything if there's
        # no sign
        amount_found = len(found)

        if amount_found != 0:

            # There may be more than one
            # sign in the image
            for (x, y, width, height) in found:
                print("Draw Rectangle")
                cv2.rectangle(img, (x, y),
                              (x + height, y + width),
                              (0, 255, 0), 5)

        # Creates the environment of
        # the picture and shows it
        #plt.subplot(1, 1, 1)
        #plt.imshow(img_rgb)
        #plt.show()
        cv2.imshow('resBlue', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


Test()
cap.release()
cv2.destroyAllWindows()

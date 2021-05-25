import numpy as np
import cv2

cap = cv2.VideoCapture(0)
def Test():

    while(True):
        ret, img = cap.read()

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([80, 100, 100])
        upper_blue = np.array([110,255,255])

        maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)

        resBlue = cv2.bitwise_and(img,img, mask= maskBlue)

        gray = cv2.cvtColor(resBlue, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]





        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img_contours = img

        max_area = 0

        max_contour = contours[0]

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if max_area < area:
                max_area = area
                max_contour = cnt

        cv2.drawContours(img_contours, [max_contour], -1, (0, 255, 255), 3)
        M = cv2.moments(max_contour)


        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv2.circle(img_contours, (cx, cy), 3, (0, 255, 255), -1)

        width = img.shape[1]

        if cx < width / 2:
            print('Left')
        else:
            print('Right')

        cv2.imshow('resBlue', img_contours)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


Test()
cap.release()
cv2.destroyAllWindows()

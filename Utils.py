import numpy as np
import cv2

dist_pix = 300


# returns left/right of the middle with how many pixels to the middle and
# up/down of the middle with how many pixels to the middle
def get_distance_blue(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([80, 100, 100])
    upper_blue = np.array([110, 255, 255])

    maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)

    resBlue = cv2.bitwise_and(img, img, mask=maskBlue)

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

    x, y, w, h = cv2.boundingRect(max_contour)
    cv2.rectangle(img_contours, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.drawContours(img_contours, [max_contour], -1, (0, 255, 255), 3)
    M = cv2.moments(max_contour)
    try:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        cv2.circle(img_contours, (cx, cy), 3, (0, 255, 255), -1)

        cv2.imshow("img", img_contours)
        cv2.waitKey(0)
        width = img.shape[1]
        height = img.shape[0]

        if cx < width / 2:
            if cy < height / 2:
                return "left", width / 2 - cx, h < dist_pix
            else:
                return "left", width / 2 - cx, "down", h < dist_pix
        else:
            if cy < height / 2:
                return "right", cx - width / 2, "up", h < dist_pix
            else:
                return "right", cx - width / 2, "down", h < dist_pix
    except:
        pass

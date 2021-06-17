import numpy as np
import cv2

distPix = 300
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import imutils as imutils

class Utils:
    def __init__(self):
        self.__interpreter = tf.lite.Interpreter("models/model.tflite")
        self.__interpreter.allocate_tensors()
        self.__inputDetails = self.__interpreter.get_input_details()
        self.__outputDetails = self.__interpreter.get_output_details()

        prototxtPath = "models/deploy.prototxt"
        weightsPath = "models/res10_300x300_ssd_iter_140000.caffemodel"
        self.__faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
    
    # grab the dimensions of the frame and then construct a blob from it
    def detectAndPredictMask(self, frame):
        global outputData
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                                     (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the face detections
        self.__faceNet.setInput(blob)
        detections = self.__faceNet.forward()

        # initialize our list of faces, their corresponding locations,and the list of predictions from our face mask network
        faces = []
        locs = []
        preds = []

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the detection
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the confidence is
            # greater than the minimum confidence
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                face = frame[startY:endY, startX:endX]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)

                # add the face and bounding boxes to their respective lists
                faces.append(face)
                locs.append((startX, startY, endX, endY))

        # only make a predictions if at least one face was detected
        if len(faces) > 0:
            faces = np.array(faces, dtype="float32")
            self.__interpreter.set_tensor(self.__input_details[0]["index"], faces)
            self.__interpreter.invoke()

            outputData = self.__interpreter.get_tensor(self.__output_details[0]["index"])

        print(outputData)
        return locs, outputData

    def hasCup(self, hierarchy, contours):
        max_area = 0
        hierarchy = hierarchy[0]
        try:
            for cnr in range(len(contours)):
                cnt = contours[cnr]
                area = cv2.contourArea(cnt)
                if max_area < area:
                    max_area = area
                    holes = 0
                    child = hierarchy[cnr][2]
                    while child >= 0:
                        holes += 1
                        child = hierarchy[child][0]
                    if holes > 0:
                        obstacle = contours[child]
                        x, y, w, h = cv2.boundingRect(obstacle)

            height = img.shape[0]

            M = cv2.moments(obstacle)
            cy = int(M['m01'] / M['m00'])

            if cy < height - 200:
                return False
            else:
                return True
        except:
            return False

    # returns left/right of the middle with how many pixels to the middle and
    # up/down of the middle with how many pixels to the middle
    # 0 = blue line
    # 1 = black line
    def getDistanceBlue(self, img, par):
        # print(img)
        print(img)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        if par == 0:
            lowerBlue = np.array([97,130,99])
            upperBlue = np.array([106,220,220])
            #upper_blue = np.array([115, 170, 255])
            #lower_blue = np.array([100, 170, 255])
        elif par == 1:
            lowerBlue = np.array([0,0,0])
            upperBlue = np.array([255,100,100])
            
        maskBlue = cv2.inRange(hsv, lowerBlue, upperBlue)

        resBlue = cv2.bitwise_and(img, img, mask=maskBlue)

        gray = cv2.cvtColor(resBlue, cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        imgContours = img
        if par == 0:
            try:
                maxArea = 0
                maxContour = contours[0]
                # Goes through all the contours and tries to find the biggest one.
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if maxArea < area:
                        maxArea = area
                        maxContour = cnt

                # Get and show the rectangle around the biggest contour.
                x, y, w, h = cv2.boundingRect(maxContour)
                cv2.rectangle(imgContours, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Show the biggest contour.
                cv2.drawContours(imgContours, [maxContour], -1, (0, 255, 255), 3)

                # Find the center of mass and show as a circle.
                M = cv2.moments(maxContour)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.circle(imgContours, (cx, cy), 3, (0, 255, 255), -1)

                cv2.imshow("img", imgContours)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return ""

                width = img.shape[1]
                height = img.shape[0]

                # Check where the biggest contour is located with a margin (dist_pix)
                if cx < width / 2:
                    if cy < height / 2:
                        return "left", width / 2 - cx, h < distPix
                    else:
                        return "left", width / 2 - cx, "down", h < distPix
                else:
                    if cy < height / 2:
                        return "right", cx - width / 2, "up", h < distPix
                    else:
                        return "right", cx - width / 2, "down", h < distPix

            except:
                cv2.imshow("img", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return ""
                return ""
        elif par == 1:
            try:
                max_area = 0
                maxContour = contours[0]
                hierarchy = hierarchy[0]

                for cnr in range(len(contours)):
                    cnt = contours[cnr]
                    area = cv2.contourArea(cnt)
                    if max_area < area:
                        max_area = area
                        max_contour = cnt

                    height = img.shape[0]
                    width = img.shape[1]

                    cv2.drawContours(imgContours, [maxContour], -1, (0, 255, 255), 3)
                    cv2.imshow("img", imgContours)

                    M = cv2.moments(maxContour)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    if cx < width / 2:
                        if cy < height / 2:
                            return "left", width / 2 - cx, self.hasCup(hierarchy, contours)
                        else:
                            return "left", width / 2 - cx, self.hasCup(hierarchy, contours), "down"
                    else:
                        if cy < height / 2:
                            return "right", cx - width / 2, self.hasCup(hierarchy, contours), "up"
                        else:
                            return "right", cx - width / 2, self.hasCup(hierarchy, contours), "down"
            except:
                cv2.imshow("img", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    return ""
                return ""


import numpy as np
import cv2

dist_pix = 300
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
    
    # returns left/right of the middle with how many pixels to the middle and
    # up/down of the middle with how many pixels to the middle
    # 0 = blue line
    # 1 = black line
    def getDistanceBlue(self, img, par):
        print(img)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        if par == 0:
            lowerBlue = np.array([99,160,99])
            upperBlue = np.array([109,255,255])
            #upper_blue = np.array([115, 170, 255])
            #lower_blue = np.array([100, 170, 255])
        elif par == 1:
            lowerBlue = np.array([0,0,0])
            upperBlue = np.array([255,50,50])
            
        maskBlue = cv2.inRange(hsv, lowerBlue, upperBlue)

        resBlue = cv2.bitwise_and(img, img, mask=maskBlue)

        gray = cv2.cvtColor(resBlue, cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        try:
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            imgContours = img

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
    
    

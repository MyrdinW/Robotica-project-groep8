import numpy as np
import cv2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import playsound

dist_pix = 300

class Utils:
    def __init__(self):
        self.maskNet = load_model("/home/pi/x/Robotica-project-groep8/models/mask_detector.model")
        # load dataset
        prototxtPath = r"/models/deploy.prototxt"
        weightsPath = r"/models/res10_300x300_ssd_iter_140000.caffemodel"
        self.faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
        
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


    # grab the dimensions of the frame and then construct a blob from it
    def detect_and_predict_mask(frame):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
                                     (104.0, 177.0, 123.0))

        # pass the blob through the network and obtain the face detections
        self.faceNet.setInput(blob)
        detections = self.faceNet.forward()
        print(detections.shape)

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
            preds = self.maskNet.predict(faces, batch_size=32)
        
        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred
        
            if mask < withoutMask:
                playsound.playsound("sounds/shallnotpass.wav")
                break

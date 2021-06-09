import cv2
import imutils

class Mask:
    """
    Mask makes the robot detect if a person is wearing a mask or not
    It uses the class Utils that uses a model of machine learning
    """
    def __init__(self, camera, utils, driver):
        self.__camera = camera
        self.__utils = utils
        self.__driver = driver
        # self.__light = Light(13)
        
    def run(self):

        # assign image to access_granted or access_denied
        access_granted = cv2.imread("/image/granted.png")
        access_denied = cv2.imread("/image/denied.png")

        # checks if the label has changed
        class ValueCache(object):
            def __init__(self, label=None):
                self.label = label

            def update(self, new_label):
                if self.label == new_label:
                    return False
                else:
                    self.label = new_label
                    return True

        # get frame from the video stream and resize it
        for i in range(200):
            frame = self.__camera.getImage()
            frame = imutils.resize(frame, width=800)

            # detect faces in the frame and determine if they are wearing a mask
            try:
                locs, preds = self.__utils.detectAndPredictMask(frame)

                value = None
                new_value = None

                for (box, pred) in zip(locs, preds):
                    (startX, startY, endX, endY) = box
                    (mask, withoutMask) = pred

                    # determine the label and color which are used to draw the box and text
                    label = "Mask" if mask > withoutMask else "No Mask"
                    if mask < withoutMask:
                        print("No mask")
                    else:
                        print("Mask")
                        # threading.Thread(target=playsound.playsound("shall.mp3")).start()

                    # set the color based on the label
                    color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

                    # inculde the probability when printing the label
                    label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

                    # displays the label and box on the output of frame
                    cv2.putText(frame, label, (startX, startY - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                    cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

                # show the image based on the label that is shown
                # check if current value has changed and show image accordingly
                if value != new_value:
                    value = new_value
                    if value == "Mask":
                        cv2.imshow("access", access_granted)
                        
                    else:
                        cv2.imshow("access", access_denied)
            except:
                pass

            # show the output of frame
            cv2.imshow("Frame", frame)

            # break the loop if 'q' is pressed
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        self.__camera.closeVideo()
        cv2.destroyAllWindows()
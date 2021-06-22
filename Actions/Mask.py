import cv2
import imutils


class Mask:
    def __init__(self, camera, utils, driver, light):
        self.__camera = camera
        self.__utils = utils
        self.__driver = driver
        self.__light = light
        self.__lastcolor = None

    class ValueCache(object):
        def __init__(self, label = None):
            self.label = label

        def update(self, new_label):
            if self.label == new_label:
                return False
            else:
                self.label = new_label
                return True

    def run(self):

        value = None
        new_value = None

        try:
            # get frame from the video stream and resize it
            frame = self.__camera.getImage()

            frame = imutils.resize(frame, width=800)

            # detect faces in the frame and determine if they are wearing a mask

            locs, preds = self.__utils.detectAndPredictMask(frame)
            # if preds == None:
            #  return
            for (box, pred) in zip(locs, preds):
                (startX, startY, endX, endY) = box
                (mask, withoutMask) = pred

                # determine the label and color which are used to draw the box and text
                label = "Mask" if mask > withoutMask else "No Mask"
                if mask < withoutMask:
                    print("No mask")
                    new_value = "n"
                else:
                    print("Mask")
                    new_value = "Mask"
                # threading.Thread(target=playsound.playsound("shall.mp3")).start()

                # set the color based on the label
                #color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

                # inculde the probability when printing the label
                #label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

                # displays the label and box on the output of frame
                #cv2.putText(frame, label, (startX, startY - 10),
                #            cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                #cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
#
                midY = (startY + endY) / 2
                midX = (startX + endX) / 2

                if midX < 50:
                    self.__driver.move(0, 0)
                    return

                if midX < 300:
                    turningspeed = midX - 400/400
                    self.__driver.move(0, turningspeed)
                    return

                elif midX > 500:

                    turningspeed = midX - 400/400
                    self.__driver.move(0, turningspeed)
                    return
#                 if midY > 390:
#                     self.__driver.moveUp()
#                 elif midY < 340:
#                     self.__driver.moveDown()

                # show the image based on the label that is shown
                # check if current value has changed and show image accordingly
                if value != new_value:
                    value = new_value
                    if value == "Mask":
                        self.__light.changeLights("g")
                        self.__lastcolor = "g"
                    elif
                    else:
                        self.__light.changeLights("r")
                        self.__lastcolor = "r"

            # show the output of frame
            #cv2.imshow("Frame", frame)

            # break the loop if 'q' is pressed
            #key = cv2.waitKey(1) & 0xFF
            #if key == ord("q"):
            #    return

                # self.__camera.closeVideo()
                # cv2.destroyAllWindows()

        except:
            pass

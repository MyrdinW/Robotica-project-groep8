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

            frame = self.__camera.getImage()
            # get frame from the video stream and resize it
            frame = imutils.resize(frame, width=800)
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

                # set the color based on the label
                color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

                # inculde the probability when printing the label
    #             label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

                # displays the label and box on the output of frame
                cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)


                # move the camera up or down
                midY = (startY + endY) / 2

                if midY > 380:
                    print("moving up")
                    print(midY)
                    self.__driver.moveUp()
                elif midY < 320:
                    print("moving down")
                    print(midY)
                    self.__driver.moveDown()

                # show the image based on the label that is shown
                # check if current value has changed and show image accordingly
                if value != new_value:
                    value = new_value
                    if value == "Mask":
                        self.__light.changeLights("g")
                        self.__lastcolor = "g"
                    else:
                        self.__light.changeLights("r")
                        self.__lastcolor = "r"

            # show the output of frame
            cv2.imshow("Frame", frame)

        except:
            pass

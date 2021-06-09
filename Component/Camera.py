import cv2


class Camera:
    """
        Class to handle camera actions
    """

    def __init__(self):
        self.__camera = cv2.VideoCapture(-1)
        self.__frame = None
        print("Camera initialized")

    def update(self):
        while True:
            _, frame = self.__camera.read()
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            self.__frame = frame

    # returns image array
    def getImage(self):
        return self.__frame

    # close video stream to re
    def closeVideo(self):
        self.__camera.release()
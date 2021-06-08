import cv2


class Camera:
    """
        Class to handle camera actions
    """

    def __init__(self):
        self.__camera = cv2.VideoCapture(-1)
        # self.__last_image = None
        print("Camera initialized")

    # returns image array
    def get_image(self):
        _, frame = self.__camera.read()

        # rotate image 180, camera is upside down due to design
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        return frame

    # close video stream to resolve "camera already in use error"
    def close_video(self):
        self.__camera.release()



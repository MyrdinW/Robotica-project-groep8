import cv2


class Camera:
    """
        Class to handle camera actions
    """

    def __init__(self):
        super().__init__()
        self.__camera = cv2.VideoCapture(-1)
        print("Camera initialized")

    # returns image array
    def get_image(self):
        return self.__camera.read()
    
    def close_video(self):
        self.__camera.release()



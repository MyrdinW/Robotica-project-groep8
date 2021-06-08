import cv2


class Camera:
    """
        Class to handle camera actions
    """

    def __init__(self):
        super().__init__()
        self.__camera = cv2.VideoCapture(-1)
        # self.__last_image = None
        print("Camera initialized")
    

            
    
    # returns image array
    def get_image(self):
        _, frame = self.__camera.read()
        frame = cv2.rotate(frame, cv2.ROTATE_180)
        return frame
    
    def close_video(self):
        self.__camera.release()



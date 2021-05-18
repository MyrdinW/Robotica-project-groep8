from Part import Part
import cv2


class Camera(Part):
    def __init__(self):
        super().__init__()
        self.camera = cv2.VideoCapture(0)

    def get_image(self):
        return self.camera.read()

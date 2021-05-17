from Part import Part
import numpy as np
import cv2


class Camera(Part):
    def __init__(self):
        try:
            super().__init__()
            size = (1920, 1080, 1)
            self.output = np.zeros(size, dtype=np.uint8)
            self.camera = cv2.VideoCapture(0)

            def get_output(self):
                return self.output

        except Exception as e:
            print("./resources/muskie.PNG" + e)

    def get_image(self):
        try:
            return self.camera.read()
        except Exception as e:
            print("./resources/muskie.PNG" + e)

# class Camera(Part):
#     def __init__(self):
#         super().__init__()
#         try:
#             self.camera = cv2.VideoCapture("./resources/muskie.PNG")
#         except Exception as e:
#             print("Could not init camera: " + e)
#
#     def get_image(self):
#         try:
#             return self.camera.read()
#         except Exception as e:
#             print("Could not read camera: " + e)

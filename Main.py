import base64
import cv2
from flask import Flask, jsonify
from flask_classful import FlaskView
from flask_cors import CORS
import warnings
from Controller import Controller

app = Flask(__name__)
CORS(app)
controller = Controller()
camera_obj, servo_obj, light_obj, engine1_obj, engine2_obj, microphone_obj, weight_obj = controller.get_components()
warnings.filterwarnings("ignore")


class ComponentsView(FlaskView):
    """
    API website to retieve component values for telemetry site
    """

    # returns encoded jpeg string of camera image
    def camera(self):
        success, image = camera_obj.get_image()
        ret, jpeg = cv2.imencode('.jpg', image)
        jpeg = base64.b64encode(jpeg)
        return jpeg

    # returns encoded jpeg string of sound wave image
    def microphone(self):
        image = microphone_obj.get_image()
        return image

    # returns value of led lights
    def light(self):
        return jsonify(light=light_obj.get_lights())

    # returns value and torgue of servo
    def servo(self):
        return jsonify(servo_value=servo_obj.get_value(), servo_torque=servo_obj.get_torque())

    # returns value and torgue of engine
    def engine(self):
        return jsonify(engine1_value=engine_obj.get_value(), engine_offset=engine1_obj.get_offset())
    
    # returns value and torgue of engine
    def engine(self):
        return jsonify(engine2_value=engine_obj.get_value(), engine_offset=engine2_obj.get_offset())

    # returns weight in grams
    def weight(self):
        return jsonify(weight=weight_obj.get_weight())


ComponentsView.register(app, route_base="/api/")

app.run()

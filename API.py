import base64
import cv2
from flask import Flask, jsonify
from flask_cors import CORS
from flask_classful import FlaskView
from Controller import Controller

app = Flask(__name__)
CORS(app)
controller = Controller()
camera_obj, servo_obj, remote_obj, light_obj, engine_obj, microphone_obj, weight_obj = controller.get_components()

class ComponentsView(FlaskView):
    def camera(self):
        success, image = camera_obj.get_image()
        ret, jpeg = cv2.imencode('.jpg', image)
        jpeg = base64.b64encode(jpeg)
        return jpeg

    def microphone(self):
        image = microphone_obj.get_image()
        return image

    def light(self):
        return jsonify(light=light_obj.get_value())

    def servo(self):
        return jsonify(servo_value=servo_obj.get_value(), servo_torque=servo_obj.get_torque())

    def engine(self):
        return jsonify(engine_value=engine_obj.get_value(), engine_offset=engine_obj.get_offset())

    def weight(self):
        print("weight")
        return jsonify(weight=weight_obj.get_weight())

ComponentsView.register(app, route_base="/api/")

app.run()

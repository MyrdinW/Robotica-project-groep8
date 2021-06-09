import base64
import cv2
from flask import Flask, jsonify
from flask_classful import FlaskView
from flask_cors import CORS
import warnings
from Controller import Controller

app = Flask(__name__)

# enable cross-origin resource sharing
CORS(app)

# make controller and retrieve different components for API-endpoint
controller = Controller()

#non pi test
# cameraObj, microphoneObj = controller.getComponents()
cameraObj, servoGripperObj, servoCameraObj, lightObj, engine1Obj, engine2Obj, microphoneObj, weightObj = controller.getComponents()
warnings.filterwarnings("ignore")


class ComponentsView(FlaskView):
    """
    API website to retieve component values for telemetry site
    """

    # returns encoded jpeg string of camera image
    def camera(self):
        image = cameraObj.getImage()
        ret, jpeg = cv2.imencode('.jpg', image)
        jpeg = base64.b64encode(jpeg)
        return jpeg

    # returns encoded jpeg string of sound wave image
    def microphone(self):
        image = microphoneObj.getImage()
        return image

    # returns value of led lights
    def light(self):
        return jsonify(light=lightObj.getLights())

    # returns value and torque of servo for camera
    def servoCamera(self):
        return jsonify(servo_value=servoCameraObj.getValue(), servo_torque=servoCameraObj.getTorque())

    # returns value and torque of servo for gripper
    def servoGripper(self):
        return jsonify(servo_value=servoGripperObj.getValue(), servo_torque=servoGripperObj.getTorque())

    # returns value and torque of engine 1
    def engine1(self):
        return jsonify(engine1_value=engine1Obj.getValue(), engine1_offset=engine1Obj.getOffset())

    # returns value and torque of engine 2
    def engine2(self):
        return jsonify(engine2_value=engine2Obj.getValue(), engine2_offset=engine2Obj.getOffset())

    # returns weight in grams
    def weight(self):
        return jsonify(weight=weightObj.getWeight())


ComponentsView.register(app, route_base="/api/")

# run site
app.run()

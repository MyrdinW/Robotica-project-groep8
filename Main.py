import base64
import cv2
from flask import Flask, jsonify, request
from flask_classful import FlaskView
from flask_cors import CORS
import warnings
from Controller import Controller
from Component.Sound import Sound

sound = Sound()

app = Flask(__name__)

# enable cross-origin resource sharing
CORS(app)

# make controller and retrieve different components for API-endpoint
controller = Controller()
cameraObj, servoObj, lightObj, engine1Obj, engine2Obj, microphoneObj, weightObj = controller.getComponents()
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

    # returns value and torgue of servo
    def servo(self):
        return jsonify(servo_value=0, servo_torque=0)

   # returns value and torgue of engine
    def engine1(self):
        return jsonify(engine1_value=engine1Obj.getValue(), engine1_offset=engine1Obj.getOffset())

    # returns value and torgue of engine
    def engine2(self):
        return jsonify(engine2_value=engine2Obj.getValue(), engine2_offset=engine2Obj.getOffset())

    # returns weight in grams
    def weight(self):
        return jsonify(weight=weightObj.getWeight())

    def sound(self):
        song = request.args.get("song")
        sound.selectSound(song)
        return ""


print("component added")
ComponentsView.register(app, route_base="/api/")

# run site
print("running site")
app.run(host='0.0.0.0', port=3999)

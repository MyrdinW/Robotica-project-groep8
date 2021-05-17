import base64
import cv2
from flask import Flask, jsonify
from flask_cors import CORS

from Controller import Controller

app = Flask(__name__)
CORS(app)
controller = Controller()
camera_obj, servo_obj, remote_obj, light_obj, engine_obj, microphone_obj = controller.get_components()


@app.route("/api/camera/")
def camera():
    print("camera")
    success, image = camera_obj.get_image()
    ret, jpeg = cv2.imencode('.jpg', image)
    jpeg = base64.b64encode(jpeg)
    # print(jpeg)
    return jpeg



@app.route("/api/microphone/")
def microphone():
    image = microphone_obj.get_image()
    #print(image)
    return image


@app.route("/api/light/")
def light():
    return jsonify(light=light_obj.get_value())


@app.route("/api/servo/", methods=['GET'])
def servo():
    return jsonify(servo_value=servo_obj.get_value(), servo_torque=servo_obj.get_torque())


@app.route("/api/engine/", methods=['GET'])
def engine():
    return jsonify(engine_value=engine_obj.get_value(), engine_offset=engine_obj.get_offset())


app.run()

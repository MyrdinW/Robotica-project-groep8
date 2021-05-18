import base64
import cv2
from flask import Flask, jsonify
from flask_cors import CORS
from flask_classful import FlaskView

from Commands.DanceCommand import DanceCommand
from Commands.FollowCarCommand import FollowCarCommand
from Commands.FollowLineCommand import FollowLineCommand
from Commands.MoveCommand import MoveCommand
from Commands.PickupMaskCommand import PickupMaskCommand
from Commands.MoveGripperCommand import MoveGripperCommand
from Controller import Controller

app = Flask(__name__)
CORS(app)
controller = Controller()
camera_obj, servo_obj, remote_obj, light_obj, engine_obj, microphone_obj, weight_obj = controller.get_components()


class ActionsView(FlaskView):
    def move(self):
        jsx1, jsx2, jsy1, jsy2 = remote_obj.get_joy_positions()
        moveCommand = MoveCommand(jsx1, jsy1, jsx2, jsy2)
        moveCommand.excecute()
        return ""

    def movegripper(self):
        jsx1, jsx2, jsy1, jsy2 = remote_obj.get_joy_positions()
        moveGripperCommand = MoveGripperCommand(jsx1, jsy1, jsx2, jsy2)
        moveGripperCommand.excecute()
        return ""

    def dance(self):
        danceCommand = DanceCommand()
        danceCommand.excecute()
        return ""

    def followline(self):
        followLineCommand = FollowLineCommand(camera_obj)
        followLineCommand.excecute()
        return ""

    def followcar(self):
        followCarCommand = FollowCarCommand(camera_obj)
        followCarCommand.excecute()
        return ""

    def pickupmask(self):
        pickupMaskCommand = PickupMaskCommand(camera_obj)
        pickupMaskCommand.excecute()
        return ""


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
        return jsonify(weight=weight_obj.get_weight())


ActionsView.register(app, route_base="/action/")
ComponentsView.register(app, route_base="/api/")

app.run()

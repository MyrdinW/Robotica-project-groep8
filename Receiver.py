import argparse
from datetime import datetime
import struct
import sys
import time
import traceback

import pigpio
from nrf24 import *
from Commands.DanceCommand import DanceCommand
from Commands.FollowCarCommand import FollowCarCommand
from Commands.FollowLineCommand import FollowLineCommand
from Commands.MoveCommand import MoveCommand
from Commands.PickupMaskCommand import PickupMaskCommand
from Commands.MoveGripperCommand import MoveGripperCommand


class Receiver:
    def __init__(self, camera, microphone):
        self.parser = argparse.ArgumentParser(prog="simple-receiver.py", description="Simple NRF24 Receiver Example.")
        self.parser.add_argument('-n', '--hostname', type=str, default='localhost',
                                 help="Hostname for the Raspberry running the pigpio daemon.")
        self.parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
        self.parser.add_argument('address', type=str, nargs='?', default='1SNSR',
                                 help="Address to listen to (3 to 5 ASCII characters)")

        self.args = self.parser.parse_args()
        self.hostname = self.args.hostname
        self.port = self.args.port
        self.address = self.args.address
        self.camera = camera
        self.microphone = microphone

        if not (2 < len(self.address) < 6):
            print(f'Invalid address {self.address}. Addresses must be between 3 and 5 ASCII characters.')
            sys.exit(1)

        print(f'Connecting to GPIO daemon on {self.hostname}:{self.port} ...')
        self.pi = pigpio.pi(self.hostname, self.port)
        if not self.pi.connected:
            print("Not connected to Raspberry Pi ... goodbye.")
            sys.exit()

        self.nrf = NRF24(self.pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100,
                         data_rate=RF24_DATA_RATE.RATE_250KBPS,
                         pa_level=RF24_PA.MAX)
        self.nrf.set_address_bytes(len(self.address))
        self.nrf.open_reading_pipe(RF24_RX_ADDR.P1, self.address)

    def listen(self):
        # Enter a loop receiving data on the address specified.
        try:
            print(f'Receive from {self.address}')
            count = 0
            while True:

                # As long as data is ready for processing, process it.
                while self.nrf.data_ready():
                    # Count message and record time of reception.
                    count += 1
                    now = datetime.now()

                    # Read pipe and payload for message.
                    pipe = self.nrf.data_pipe()
                    payload = self.nrf.get_payload()

                    # Resolve protocol number.
                    protocol = payload[0] if len(payload) > 0 else -1

                    hex = ':'.join(f'{i:02x}' for i in payload)

                    # Show message received as hex.
                    print(
                        f"{now:%Y-%m-%d %H:%M:%S.%f}: pipe: {pipe}, len: {len(payload)}, bytes: {hex}, count: {count}")

                    # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
                    # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
                    if len(payload) == 9 and payload[0] == 0x01:
                        values = struct.unpack("<Bff", payload)
                        if values[0] == "dance":
                            danceCommand = DanceCommand()
                            danceCommand.excecute()
                        if values[0] == "followline":
                            followLine = FollowLineCommand(self.camera)
                            followLine.excecute()
                        if values[0] == "move":
                            js1x = values[1]
                            js2x = values[2]
                            js1y = values[3]
                            js2y = values[4]
                            moveCommand = MoveCommand(js1x, js2x, js1y, js2y)
                            moveCommand.excecute()
                        if values[0] == "movegripper":
                            js1x = values[1]
                            js2x = values[2]
                            js1y = values[3]
                            js2y = values[4]
                            moveGripperCommand = MoveGripperCommand(js1x, js2x, js1y, js2y)
                            moveGripperCommand.excecute()
                        if values[0] == "pickupmask":
                            pickupMaskCommand = PickupMaskCommand(self.camera)
                            pickupMaskCommand.excecute()


                # Sleep 100 ms.
                time.sleep(0.1)
        except:
            traceback.print_exc()
            self.nrf.power_down()
            self.pi.stop()

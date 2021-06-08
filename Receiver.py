import argparse
import datetime
import sys
import pigpio
import RPi.GPIO as GPIO
from nrf24 import *


class Receiver:
    """
    Handles remote signals
    """
    def __init__(self):
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)    
        GPIO.output(21, 1)
        
        
        
        parser = argparse.ArgumentParser(prog="Receiver.py", description="Simple NRF24 Receiver Example.")
        parser.add_argument('-n', '--hostname', type=str, default='localhost',
                            help="Hostname for the Raspberry running the pigpio daemon.")
        parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
        parser.add_argument('address', type=str, nargs='?', default='ROBBY',
                            help="Address to listen to (3 to 5 ASCII characters)")

        self.args = parser.parse_args()
        self.hostname = self.args.hostname
        self.port = self.args.port
        self.address = self.args.address

        if not (2 < len(self.address) < 6):
            print(f'Invalid address {self.address}. Addresses must be between 3 and 5 ASCII characters.')
            sys.exit(1)

        print(f'Connecting to GPIO daemon on {self.hostname}:{self.port} ...')
        self.pi = pigpio.pi(self.hostname, self.port)
        if not self.pi.connected:
            print("Not connected to Raspberry Pi ... goodbye.")
            sys.exit()

        self.__nrf = NRF24(self.pi, ce=5, payload_size=RF24_PAYLOAD.DYNAMIC, channel=69,
                           data_rate=RF24_DATA_RATE.RATE_2MBPS, pa_level=RF24_PA.MAX)
        self.__nrf.set_address_bytes(len(self.address))
        self.__nrf.open_reading_pipe(RF24_RX_ADDR.P1, self.address)

        print("Receiver initialized")

    # Returns command received from remote
    def listen(self):
        # Enter a loop receiving data on the address specified.
        count = 0
        self.now = datetime.datetime.now()

        # As long as data is ready for processing, process it.
        if self.__nrf.data_ready():
            # Count message and record time of reception.
            count += 1
            payload = str(self.__nrf.get_payload())
            # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
            # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
            comp = payload.split("b'")[1].replace("')", "").split(",")
            if comp[0] == '00':
                if len(comp) > 1:
                    comp = comp[1:]
                   
                    return comp
        else:
            return None

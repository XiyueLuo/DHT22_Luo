import time
import board
#import adafruit_dht
import array
import time
import digitalio
from microcontroller import Pin

# Initial the dht device, with data pin connected to:
#dhtDevice = adafruit_dht.DHT22(board.D7)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

while True:
    try:
        # Print the values to the serial port
        pulses = array.array("H")
        with digitalio.DigitalInOut(board.D7) as dhtpin:
            # we will bitbang if no pulsein capability
            transitions = []
            # Signal by setting pin high, then low, and releasing
            dhtpin.direction = digitalio.Direction.OUTPUT
            dhtpin.value = True
            time.sleep(0.1)
            dhtpin.value = False
            # Using the time to pull-down the line according to DHT Model
            time.sleep(800 / 1000000)
            timestamp = time.monotonic()  # take timestamp
            dhtval = True  # start with dht pin true because its pulled up
            dhtpin.direction = digitalio.Direction.INPUT
            print(dhtpin.value)
            '''
            try:
                dhtpin.pull = digitalio.Pull.UP
            # Catch the NotImplementedError raised because
            # blinka.microcontroller.generic_linux.libgpiod_pin does not support
            # internal pull resistors.
            except NotImplementedError:
                dhtpin.pull = None
            '''
            while time.monotonic() - timestamp < 0.25:
                if dhtval != dhtpin.value:
                    dhtval = not dhtval  # we toggled
                    transitions.append(time.monotonic())  # save the timestamp
            # convert transtions to microsecond delta pulses:
            # use last 81 pulses
            transition_start = max(1, len(transitions) - 81)
            print(transition_start)
            for i in range(transition_start, len(transitions)):
                pulses_micro_sec = int(1000000 * (transitions[i] - transitions[i - 1]))
                pulses.append(min(pulses_micro_sec, 65535))
            print(len(pulses), "pulses:", [x for x in pulses])
        '''
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        '''

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)

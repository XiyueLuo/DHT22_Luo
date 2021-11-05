# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_dht
import array
import time
import pulseio
from microcontroller import Pin

# Initial the dht device, with data pin connected to:
pulse_in = PulseIn(board.D7, maxlen=81, idle_state=True)
dhtDevice = adafruit_dht.DHT22(board.D7)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

while True:
    try:
        # Print the values to the serial port
        pulses = array.array("H")
        pulse_in.clear()
        pulse_in.resume(800)

        # loop until we get the return pulse we need or
        # time out after 1/4 second
        time.sleep(0.25)
        pulse_in.pause()
        while pulse_in:
            pulses.append(pulse_in.popleft())
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

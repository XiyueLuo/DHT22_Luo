import os
import pigpio
import sys
import time
os.chdir("/home/pi/pigpio_dht22")  # so that new module is in the right path
sys.path.append("/home/pi/pigpio_dht22")
import DHT22

class TempHumiditySensor():
    def __init__(self, gpio=4):
        self.gpio = gpio
        self.pi = pigpio.pi()
        self.s = DHT22.sensor(self.pi, self.gpio)

    def read_value(self):
        self.s.trigger()
        while self.s.humidity() == -999 and self.s.temperature() == -999:
            time.sleep(1)
        if self.s.humidity() is not None and self.s.temperature() is not None:
            farenheit = self.s.temperature()
            humidity = self.s.humidity()
            #farenheit = (farenheit * 1.8) + 32
            return humidity,farenheit
        else:
            return "error"

    def calibrate(self, calib_val_humidity, calib_val_temperature):
        humidity, temperature = self.read_value()
        self.calib_humidity = calib_val_humidity - humidity
        self.calib_temperature = calib_val_temperature - temperature
        pass

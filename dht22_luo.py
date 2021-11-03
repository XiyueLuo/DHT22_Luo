from time import sleep
from temphumidity import TempHumiditySensor

sensor = TempHumiditySensor()
while True:
    (humidity,temp) = sensor.read_value()
    print(humidity,temp)
    sleep(20)


## Author Conor O'Kelly
## Echo sensor

#from sensors.SensorInterface import Sensor
import RPi.GPIO as GPIO
import time
import datetime

class EchoSensor():

    def __init__(self,sensorName, TRIG=16, ECHO=19, GpioMode=GPIO.BCM, warnings=False):

        self.sensorName = sensorName
        self.trig = TRIG
        self.echo = ECHO
        self.gpioMode = GpioMode
        self.warnings = warnings
        self._setup()

        ### Main Varibles ###
        self._speedOfSound = 34_300 # m/s
        self._timeOfMeasurement = 0
        self._sensorMaxWait = 1_000
        self._maxDistance = 300
        self._maxDistanceWait = (self._maxDistance / self._speedOfSound) * 1.1 # Second to wait before ingorning return result

    def _setup(self):

        # Set warning to false
        GPIO.setwarnings(self.warnings)
        # Set mode
        GPIO.setmode(self.gpioMode)
        # Set sensors
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

        # Settle the trigger and wait
        GPIO.output(self.trig, False)
        time.sleep(0.2)
        GPIO.output(self.trig, True)
        time.sleep(0.2)
        GPIO.output(self.trig, False)

    def getData(self):

        # Reset error. TODO refactor out global var
        self.error = "None" 

        distance = self._calculateDistance()
        time = str(self._timeOfMeasurement)

        return {"sensorName":self.sensorName, "distance":distance, "time":time, "settleWaitCount":self._settleWaitCount, "error":self.error}

    def _calculateDistance(self):

        # Start moudle program
        GPIO.output(self.trig,True)
        time.sleep(0.00001)
        GPIO.output(self.trig,False)

        pulse_start = time.time()
        pulse_end = time.time()

        # TODO set properly
        self._timeOfMeasurement = pulse_start

        self._settleWaitCount = 0
        while (GPIO.input(self.echo) == 0):
            self._settleWaitCount += 1
            if (self._settleWaitCount > self._sensorMaxWait):
                self.error = "Sensor did not start correctly"
                return 0

            pulse_start = time.time()

        # Time out if wait is too long
        while (GPIO.input(self.echo) == 1 and (pulse_end - pulse_start) < self._maxDistanceWait):
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        # print(pulse_duration)
        distance = self._convertDistance(pulse_duration)

        # Check if count settled to quiclky
        if self._settleWaitCount < 10:
            self.error = "Sesnor settled to quickly"
            return 0

        if distance > self._maxDistance:
            self.error = "Over max distance"
            return 0
        else:
            return distance

    def _convertDistance(self, pulse_duration):
        distance = pulse_duration * self._speedOfSound / 2 # Round trip
        return distance

    def __repr__(self):
        return ("SensorInterface object. Trig ="+str(self.trig)+" Echo="+str(self.echo)+".")

if (__name__ == '__main__'):

    sensor = DistanceSensor("Test")
    info = sensor.getData()
    print(info)

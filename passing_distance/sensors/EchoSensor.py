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
        self._setup();

        self._timeOfMeasurement = 0
        self._sensorMaxWait = 1_000
        self._maxDistance = 400

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

        distance = self._calculateDistance()
        time = str(self._timeOfMeasurement)

        return {"sensorName":self.sensorName, "distance":distance, "time":time}

    def _calculateDistance(self):

        distance = -1

        # Start moudle program
        GPIO.output(self.trig,True)
        time.sleep(0.00001)
        GPIO.output(self.trig,False)

        pulse_start = time.time()
        pulse_end = time.time()

        # TODO set properly
        self._timeOfMeasurement = pulse_start

        waitCount = 0
        while (GPIO.input(self.echo) == 0):
            waitCount += 1
            if (waitCount > self._sensorMaxWait):
                return -3
            pulse_start = time.time()

        while (GPIO.input(self.echo) == 1 and (pulse_end - pulse_start) < 0.025):
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        # print(waitCount," count")
        # print(pulse_duration)
        distance = self._convertDistance(pulse_duration)

        # Check if count settled to quiclky
        # print(waitCount, distance)
        if waitCount < 10:
            return -2

        if distance > self._maxDistance:
            return 1000
        else:
            return distance

    def _convertDistance(self, pulse_duration):

        # Speed of sound = 34300 m/s. Round trip
        distance = pulse_duration * 34300 / 2
        return distance


    def __repr__(self):

        return ("SensorInterface object. Trig ="+str(self.trig)+" Echo="+str(self.echo)+".")

if (__name__ == '__main__'):

    sensor = DistanceSensor("Test")

    info = sensor.getData()
    print(info)

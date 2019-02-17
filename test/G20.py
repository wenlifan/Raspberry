# coding=utf-8
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)     # 超声波传感器
GPIO.setup(21, GPIO.IN)     # 超声波传感器
GPIO.setup(6, GPIO.OUT)

try:
    while True:
        a = GPIO.input(20)
        print(a)
        if GPIO.input(20):
            print("input high")
            GPIO.output(6, GPIO.LOW)
        else:
            print("input low")
            GPIO.output(6, GPIO.HIGH)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
GPIO.cleanup()
# coding=utf-8
import time
import RPi.GPIO as GPIO

GIO = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(GIO, GPIO.IN)

# p = GPIO.PWM(GIO, 50)
# p.start(0)
try:
    while 1:
        # for dc in range(0, 101, 5):
        #     p.ChangeDutyCycle(dc)
        #     time.sleep(0.1)
        # for dc in range(100, -1, -5):
        #     p.ChangeDutyCycle(dc)
        #     time.sleep(0.1)
        time.sleep(0.1)
        v_io = GPIO.input(GIO)
        if not v_io:
            print(v_io)

except KeyboardInterrupt:
    pass
# p.stop()
GPIO.cleanup()
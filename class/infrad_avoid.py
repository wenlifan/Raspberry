#!/usr/bin/python
# coding=utf-8
#本段代码实现树莓派智能小车的红外避障效果
#代码使用的树莓派GPIO是用的BOARD编码方式。
import RPi.GPIO as GPIO
from motion import Move
import time
import sys

SensorRight = 16
SensorLeft  = 12

BtnPin  = 19
Gpin    = 5
Rpin    = 6

# 移动类的实例化，及初始化
MyMontion = Move()
MyMontion.init_GPIO()

def getmembers(klass, members=None):
    # get a list of all class members, ordered by class
    if members is None:
        members = []
    for m in dir(klass):
        if m not in members:
            members.append(m)
print(getmembers(MyMontion))

def keysacn():
    val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == False:
        val = GPIO.input(BtnPin)
    while GPIO.input(BtnPin) == True:
        time.sleep(0.01)
        val = GPIO.input(BtnPin)
        if val == True:
            GPIO.output(Rpin,1)
            while GPIO.input(BtnPin) == False:
                GPIO.output(Rpin,0)
        else:
            GPIO.output(Rpin,0)

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
    GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
    GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.setup(SensorRight,GPIO.IN)
    GPIO.setup(SensorLeft,GPIO.IN)

if __name__ == '__main__':
    setup()
    keysacn()
    try:
        while True:
            SR_2 = GPIO.input(SensorRight)
            SL_2 = GPIO.input(SensorLeft)
            if SL_2 == True and SR_2 == True:
                # print "t_up"
                MyMontion.t_up(50,0)
            elif SL_2 == True and SR_2 ==False:
                # print "Left"
                MyMontion.t_left(50,0)
            elif SL_2==False and SR_2 ==True:
                # print "Right"
                MyMontion.t_right(50,0)
            else:
                MyMontion.t_stop(0.3)
                MyMontion.t_down(50,0.4)
                MyMontion.t_left(50,0.5)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        GPIO.cleanup()

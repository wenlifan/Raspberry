#!/usr/bin/env python
# coding=utf-8
# 超声波传感器,测距

import sys
import RPi.GPIO as GPIO
import time
sys.path.append('../class/');
from cl_ultrasonic import Ultrasonic

# 实例化类
MyUl = Ultrasonic()

def setup():
	MyUl.init_GPIO()

def distance():
	MyUl.distance()

def loop():
	MyUl.loop()

def destroy():
	MyUl.__del__()

if __name__ == "__main__":
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()

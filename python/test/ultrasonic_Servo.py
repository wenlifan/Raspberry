#!/usr/bin/env python
# coding=utf-8
# 本模块用于测试时 cl_motion.py

import sys
sys.path.append('../class/');
import MotorHAT
from cl_motion import Move
from MotorHAT.Adafruit_PWM_Servo_Driver import PWM
import RPi.GPIO as GPIO
import time

BtnPin  = 19
Gpin    = 5
Rpin    = 6

TRIG = 20
ECHO = 21

R_IO = 16
L_IO = 12

# 移动类的实例化，及初始化
MyMontion = Move()
MyMontion.init_GPIO()

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40,debug = False)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
	pulseLength = 1000000.0                   # 1,000,000 us per second
	pulseLength /= 50.0                       # 60 Hz
	print ("%d us per period" % pulseLength)
	pulseLength /= 4096.0                     # 12 bits of resolution
	print ("%d us per bit" % pulseLength)
	pulse *= 1000.0
	pulse /= (pulseLength*1.0)
	# pwmV=int(pluse)
	print ("pluse: %f  " % (pulse))
	pwm.setPWM(channel, 0, int(pulse))

#Angle to PWM
def write(servonum,x):
	y=x/90.0+0.5
	y=max(y,0.5)
	y=min(y,2.5)
	setServoPulse(servonum,y)

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
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)

	GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
	GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)

	GPIO.setup(R_IO,GPIO.IN)		# 右接近传感器
	GPIO.setup(L_IO,GPIO.IN)		# 左接近传感器
	pwm.setPWMFreq(50)                        # Set frequency to 60 Hz

def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)


	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def front_detection():
	write(0,90)
	time.sleep(0.5)
	dis_f = distance()
	return dis_f

def left_detection():
	write(0, 175)
	time.sleep(0.5)
	dis_l = distance()
	return dis_l

def right_detection():
	write(0,5)
	time.sleep(0.5)
	dis_r = distance()
	return dis_r

def loop():
	while True:
		r_va = int(GPIO.input(R_IO))
		l_va = int(GPIO.input(L_IO))
		if not r_va:
			print("R",r_va)
			MyMontion.t_stop(0.2)
			MyMontion.t_down(50,0.5)
			MyMontion.t_left(50,1)
		if not l_va:
			print("L",l_va)
			MyMontion.t_stop(0.2)
			MyMontion.t_down(50,0.5)
			MyMontion.t_right(50,0.3)
		dis1 = front_detection()
		if (dis1 < 40) == True:
			MyMontion.t_stop(0.2)
			MyMontion.t_down(50,0.5)
			MyMontion.t_stop(0.2)
			dis2 = left_detection()
			dis3 = right_detection()
			if (dis2 < 40) == True and (dis3 < 40) == True:
				MyMontion.t_left(50,1)
			elif (dis2 > dis3) == True:
				MyMontion.t_left(50,0.3)
				MyMontion.t_stop(0.1)
			else:
				MyMontion.t_right(50,0.3)
				MyMontion.t_stop(0.1)
		else:
			MyMontion.t_up(30,0)
			#  print dis1, 'cm'
			# print ''

def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	setup()
	keysacn()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()

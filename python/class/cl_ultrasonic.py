#!/usr/bin/python
# coding=utf-8
'''
    Ultrasonic: 使用红外遥控器控制小车,
    __init__ 中 使用了默认的端口, 没有使用传入配置, 后期需要修改.
    PWMA: 控制的方式控制小车的运动速度.
    __del__: 清楚使用的端口
'''
import lirc as pylirc
import RPi.GPIO as GPIO
import time

class Ultrasonic:
    def __init__(self):
        # 初始化的端口 BCM模式
        print("初始化的端口 BCM模式")
        self.TRIG = 20      # 输出
        self.ECHO = 21      # 输入

    def init_GPIO(self):
        print("init_GPIO")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def distance(self):
        GPIO.output(self.TRIG, 0)
        time.sleep(0.000002)

        GPIO.output(self.TRIG, 1)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, 0)

        while GPIO.input(self.ECHO) == 0:
            a = 0
        time1 = time.time()
        while GPIO.input(self.ECHO) == 1:
            a = 1
        time2 = time.time()

        during = time2 - time1
        return during * 340 / 2 * 100

    def loop(self):
        while True:
            dis = self.distance()
            print (dis, 'cm')
            print ('')
            time.sleep(0.3)

    def __del__(self):
        GPIO.cleanup([20,21])

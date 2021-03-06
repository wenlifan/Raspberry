#!/usr/bin/python
# coding=utf-8
'''
    Move: 是一个控制运动的类, __init__ 中 使用了默认的端口,
没有使用传入配置, 后期需要修改.
    PWMA: 控制的方式控制小车的运动速度.
    __del__: 清楚使用的端口
'''

import lirc as pylirc
import time
import RPi.GPIO as GPIO

# 控制小车的运动(固定了使用的IO口)
class Move:
    def __init__(self):
        # 初始化的端口 BCM模式
        print("初始化的端口 BCM模式")
        self.PWMA   = 18
        self.AIN1   = 22
        self.AIN2   = 27

        self.PWMB   = 23
        self.BIN1   = 25
        self.BIN2   = 24

    def init_GPIO(self):
        print("init_GPIO")
        GPIO.setmode(GPIO.BCM)

        # 运动GPIO准备
        print("self.AIN2 = ",self.AIN2)
        GPIO.setup(self.AIN2,GPIO.OUT)
        GPIO.setup(self.AIN1,GPIO.OUT)
        GPIO.setup(self.PWMA,GPIO.OUT)

        GPIO.setup(self.BIN1,GPIO.OUT)
        GPIO.setup(self.BIN2,GPIO.OUT)
        GPIO.setup(self.PWMB,GPIO.OUT)

        # PWM 准备
        self.L_Motor= GPIO.PWM(self.PWMA,100)
        self.L_Motor.start(0)
        self.R_Motor = GPIO.PWM(self.PWMB,100)
        self.R_Motor.start(0)

    # 前进
    def t_up(self,speed,t_time):
    	self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2,False)#AIN2
        GPIO.output(self.AIN1,True) #AIN1
        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2,False)#BIN2
        GPIO.output(self.BIN1,True) #BIN1
        time.sleep(t_time)
    # 停止
    def t_stop(self,t_time):
        self.L_Motor.ChangeDutyCycle(0)
        GPIO.output(self.AIN2,False)#AIN2
        GPIO.output(self.AIN1,False) #AIN1

        self.R_Motor.ChangeDutyCycle(0)
        GPIO.output(self.BIN2,False)#BIN2
        GPIO.output(self.BIN1,False) #BIN1
        time.sleep(t_time)

    # 后退
    def t_down(self,speed,t_time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2,True)#AIN2
        GPIO.output(self.AIN1,False) #AIN1

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2,True)#BIN2
        GPIO.output(self.BIN1,False) #BIN1
        time.sleep(t_time)

    # 左转
    def t_left(self,speed,t_time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2,True)#AIN2
        GPIO.output(self.AIN1,False) #AIN1

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2,False)#BIN2
        GPIO.output(self.BIN1,True) #BIN1
        time.sleep(t_time)

    # 右转
    def t_right(self,speed,t_time):
        self.L_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.AIN2,False)#AIN2
        GPIO.output(self.AIN1,True) #AIN1

        self.R_Motor.ChangeDutyCycle(speed)
        GPIO.output(self.BIN2,True)#BIN2
        GPIO.output(self.BIN1,False) #BIN1
        time.sleep(t_time)

    def __del__(self):
        GPIO.cleanup([18,22,27,23,25,24])

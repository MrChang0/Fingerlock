import RPi.GPIO as GPIO
import threading

GPIO.setmode(GPIO.BOARD)

channel = 12

GPIO.setup(channel, GPIO.OUT,initial=GPIO.HIGH)

def unlock():
    GPIO.output(channel,GPIO.LOW)
    threading.Timer(3,lock)

def lock():
    GPIO.output(channel,GPIO.HIGH)
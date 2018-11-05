import RPi.GPIO as GPIO
import gevent

GPIO.setmode(GPIO.BOARD)

channel = 12

GPIO.setup(channel, GPIO.OUT,initial=GPIO.LOW)

def lock():
    GPIO.output(channel,GPIO.LOW)

def unlock():
    GPIO.output(channel,GPIO.HIGH)
    gevent.sleep(3)
    lock()

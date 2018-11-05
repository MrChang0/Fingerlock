import RPi.GPIO as GPIO
import gevent

GPIO.setmode(GPIO.BOARD)

channel = 16

GPIO.setup(channel, GPIO.OUT,initial=GPIO.HIGH)

def stop():
    GPIO.output(channel,GPIO.HIGH)

def ring():
    GPIO.output(channel,GPIO.LOW)
    gevent.sleep(3)
    stop()

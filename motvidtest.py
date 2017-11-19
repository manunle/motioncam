import io
import random
import picamera
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)         #Read output from PIR motion sensor
imgWidth     = 1640                                              # Max = 2592
imgHeight    = 1232     
motiondetbef = False                                         # Max = 1944

def motion_detected():
#    return random.randint(0, 10) == 0
    global motiondetbef
    i=GPIO.input(7)
    if i==1:
	if motiondetbef == False:
            motiondetbef = True
            return True
    else:
        motiondetbef = False
    return False

camera = picamera.PiCamera()
camera.resolution = (1640,1232)
stream = picamera.PiCameraCircularIO(camera, seconds=20)
camera.start_recording(stream, format='h264')
try:
    while True:
        camera.wait_recording(1)
        if motion_detected():
            print "saving"
            # Keep recording for 10 seconds and only then write the
            # stream to disk
            camera.wait_recording(15)
            fname=time.strftime("/motionimg/%Y%m%d%H%M%S.h264")
            stream.copy_to(fname)
finally:
    camera.stop_recording()

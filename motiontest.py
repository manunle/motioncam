import RPi.GPIO as GPIO
import time
import os
import picamera

motsense = 0
motionevent = 0
imgWidth     = 1640                                              # Max = 2592
imgHeight    = 1232                                              # Max = 1944
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)         #Read output from PIR motion sensor

def on_callback(channel):
	global motionevent
	motionevent = 1
	print("motion on")

def off_callback(channel):
	print("motion off")

GPIO.add_event_detect(7,GPIO.FALLING,callback=on_callback,bouncetime=300)

frames = 60

def filenames():
    global motionevent
    frame = 0
    fname = "static.jpg"
    while True:
	if motionevent == 1:
            fname=time.strftime("/motionimg/%Y%m%d%H%M%S.jpg")
            frame += 1
            if frame > 20:
                frame = 0
                motionevent = 0
        else:
            fname="static.jpg"
        yield fname
        time.sleep(.1)        
	
def takepics():
    with picamera.PiCamera(framerate=1) as camera:
        camera.resolution = (1640,1232)
        camera.start_preview()
# calibrate the camera, this needs to be longer at night
        time.sleep(2)
        start = time.time()
        camera.capture_sequence(filenames(), use_video_port=True)
        finish = time.time()
    print('Captured %d frames at %.2ffps' % (frames,frames / (finish - start)))


takepics()
while True:
    try:  
       i=GPIO.input(7)
       if i==0:                 #When output from motion sensor is LOW
          if motsense==1:
              print "No intruders",i
              motsense=0
       elif i==1:               #When output from motion sensor is HIGH
          if motsense==0:
              motsense=1
#              takepics()
              print "Intruder detected",i
          time.sleep(0.1)
   
    except KeyboardInterrupt:  
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()  

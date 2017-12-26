#!/usr/bin/env python

import ConfigParser
import io
import random
import picamera
import RPi.GPIO as GPIO
import time

print "starting motionvid"
config = ConfigParser.RawConfigParser()
## uncomment this to create the config file
#config.add_section('Paths')
#config.set('Paths','video_directory','/motionimg/')
#config.add_section('Settings')
#config.set('Settings','MotionPin','7')
#config.set('Settings','VideoWidth','1640')
#config.set('Settings','VideoHeight','1232')
#config.set('Settings','VideoFileName','%Y%m%d%H%M%S.h264')
#config.set('Settings','VideoFormat','h264')

#with open('motionvid.conf','wb') as configfile:
#    config.write(configfile)

config.read('/home/pi/motioncam/motionvid.conf')
video_directory = config.get('Paths','video_directory')
MotionPin = int(config.get('Settings','MotionPin'))
VideoWidth = int(config.get('Settings','VideoWidth'))
VideoHeight = int(config.get('Settings','VideoHeight'))
VideoFileName = config.get('Settings','VideoFileName')
VideoFormat = config.get('Settings','VideoFormat')
VideoLength = int(config.get('Settings','VideoLength'))
AllowRetrigger = (config.get('Settings','AllowRetrigger') == 'yes')
vFlip = (config.get('Settings','vFlip') == 'no')
hFlip = (config.get('Settings','hFlip') == 'no')
expMode = (config.get('Settings','expMode') == 'night')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(MotionPin, GPIO.IN)         #Read output from PIR motion sensor
imgWidth     = VideoWidth                                             # Max = 2592
imgHeight    = VideoHeight     
motiondetbef = False                                         # Max = 1944

def motion_detected():
#    return random.randint(0, 10) == 0
    global motiondetbef
    global AllowRetrigger
    i=GPIO.input(7)
    if i==1:
	if motiondetbef == False:
            if AllowRetrigger == False:
                motiondetbef = True
            return True
    else:
        motiondetbef = False
    return False

camera = picamera.PiCamera()
camera.resolution = (1640,1232)
if(vFlip == 'yes'):
    camera.vflip = True
if(hFlip == 'yes'):
    camera.hflip = True
camera.exposure_mode = expMode
stream = picamera.PiCameraCircularIO(camera, seconds=30)
camera.start_recording(stream, format=VideoFormat)
try:
    while True:
        camera.wait_recording(1)
        if motion_detected():
            print "Capturing"
            # Keep recording for 10 seconds and only then write the
            # stream to disk
            camera.wait_recording(VideoLength)
            fname=time.strftime(video_directory + VideoFileName)
            print 'Saving'
            stream.copy_to(fname)
            print "Done saving"
finally:
    camera.stop_recording()

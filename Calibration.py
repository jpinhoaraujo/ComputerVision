#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Calibration.py
#  
#  Copyright 2021  <pi@raspberrypi>

from time import sleep
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

def InitCameraPreview():
    camera = PiCamera(resolution=(1640,922), framerate=30, sensor_mode=5)   # Start a camera object
    camera.start_preview()  # Start a preview
    sleep(2)    # Camera warm-up time
    return camera
    
def StopCameraPreview(camera):
    camera.stop_preview()
    camera.close()
    pass

def PrintCurrentSettings(camera):
    # print("Previewing: {0}".format(camera.previewing))
    print("ISO: {0}".format(camera.iso))
    print("Shutter Speed: {0}".format(camera.exposure_speed))
    print("Exposure Compensation: {0}".format(camera.exposure_compensation))
    print("AWB Gains: {0}".format(camera.awb_gains))
    print("Analog Gain: {0}, Digital Gain: {1}".format(camera.analog_gain, camera.digital_gain))
    pass

def MyCalibrationRoutine(camera):
    camera.iso = 400
    
    # Exposure mode: 'off';'auto';'night';'nightpreview';'backlight'
    # 'spotlight';'sports';'snow';'beach';'verylong';'fixedfps'
    # 'antishake'; 'fireworks'
    camera.exposure_mode = 'auto'
    
    # awb_mode:'off', 'auto', 'sunlight', 'cloudy', 'shade', 'tungsten',
    # 'fluorescent', 'incandescent', 'flash', 'horizon'
    camera.awb_mode = 'auto'
    # camera.awb_gains = (0,0)
    # camera.awb_gains = (i,i)
    
    # camera.iso = 400 # Fixed ISO for indoor low indirect light
    # cam_iso = 100 + (i*100)
    # camera.iso = cam_iso
    # cam_iso = 100 + (i*100)
    # camera.iso = cam_iso
    # camera.analog_gain
    # camera.digital_gain
    
    camera.exposure_compensation = 0
    # camera.exposure_compensation = -25 + 5*i
    
    
    camera.shutter_speed = 0
    # camera.shutter_speed = 10000 + i*1000
    
    # Fix camera parameters for exposure and awb
    # sleep(2)
    # shutter_var = camera.exposure_speed
    # camera.exposure_mode = 'off'
    # shutter_speed = shutter_var
    # (r,b) = camera.awb_gains
    # camera.awb_mode = 'off'
    # camera.awb_gains = (r,b)

    sleep(2)
    for i in range(10):
        sleep(2)
        MyCaptureRoutine(camera, i)
        PrintCurrentSettings(camera)
        sleep(0.5)
    pass
    
def MyCaptureRoutine(camera, i):
    camera.capture('ISO%s.jpg' % i, resize=(3280,2464), use_video_port=False)    # Start a capture with the still port at full resolution
    pass

def main(args):
    camera = InitCameraPreview()
    MyCalibrationRoutine(camera)
    StopCameraPreview(camera)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

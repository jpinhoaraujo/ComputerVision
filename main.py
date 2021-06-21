#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
from tracker import *
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
from io import BytesIO

# Create tracker object
tracker = Tracker()

with open(r'/home/pi/Desktop/OrangeMask.txt') as f:
    contentsOrange = f.read()
    f.close()

with open(r'/home/pi/Desktop/YellowMask.txt') as f:
    contentsYellow = f.read()
    f.close()

with open(r'/home/pi/Desktop/GreenMask.txt') as f:
    contentsGreen = f.read()
    f.close()


camera = PiCamera(resolution=(1920,1088), framerate=30, sensor_mode=5)   # Start a camera object

numberOrange=0
numberYellow=0
numberGreen=0

while True:
    rawCapture = PiRGBArray(camera, size=camera.resolution)
    camera.capture(rawCapture, format="bgr", use_video_port=False)
    frame = rawCapture.array
    height, width, _ = frame.shape
    
    roi = frame[400: 600, 200: 1800]
    
    hsv=cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # Extract Region of interest


    # 1. Object Detection

    xOrange = contentsOrange.split()
    # str(xOrange)

    LowerRegionOrange = np.array([xOrange[0], xOrange[1], xOrange[2]], np.uint8)
    upperRegionOrange = np.array([xOrange[3], xOrange[4], xOrange[5]], np.uint8)
    ObjectOrange = cv2.inRange(hsv, LowerRegionOrange, upperRegionOrange)
    edgesOrange = cv2.Canny(ObjectOrange, 100, 200)
    # cv2.imshow("Edges", edgesOrange)
    contoursOrange, _ = cv2.findContours(edgesOrange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #mask = object_detector.apply(roi)
    #_, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    #contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detectionsOrange = []
    for cnt in contoursOrange:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 1500:
            print(area)
            cv2.drawContours(hsv, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)


            detectionsOrange.append([x, y, w, h])

    # 2. Object Tracking
            boxes_ids = tracker.tracking_update(detectionsOrange)
            for box_id in boxes_ids:
                x, y, w, h, id = box_id
                cv2.putText(roi, "Orange id:"+str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 128, 255), 2)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 128, 255), 3)
                print("Number of Orange pieces: "+str(id+1))
                numberOrange=id+1





########################################################################################################################
    # 1. Object Detection YELLOW

    xYellow = contentsYellow.split()
    # str(xOrange)

    LowerRegionYellow = np.array([xYellow[0], xYellow[1], xYellow[2]], np.uint8)
    upperRegionYellow = np.array([xYellow[3], xYellow[4], xYellow[5]], np.uint8)
    ObjectYellow = cv2.inRange(hsv, LowerRegionYellow, upperRegionYellow)
    edgesYellow = cv2.Canny(ObjectYellow, 100, 200)
    # cv2.imshow("Edges", edgesOrange)
    contoursYellow, _ = cv2.findContours(edgesYellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    detectionsYellow = []
    for cnt in contoursYellow:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 1500:
            print(area)
            cv2.drawContours(hsv, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)

            detectionsYellow.append([x, y, w, h])

            # 2. Object Tracking
            boxes_ids = tracker.tracking_update(detectionsYellow)
            for box_id in boxes_ids:
                x, y, w, h, id = box_id
                cv2.putText(roi, "Yellow id:" + str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 255), 3)
                print("Number of Yellow pieces: " + str(id + 1))
                numberYellow = id + 1

        ########################################################################################################################
        # 1. Object Detection GREEN

        xGreen = contentsGreen.split()


        LowerRegionGreen = np.array([xGreen[0], xGreen[1], xGreen[2]], np.uint8)
        upperRegionGreen = np.array([xGreen[3], xGreen[4], xGreen[5]], np.uint8)
        ObjectGreen = cv2.inRange(hsv, LowerRegionGreen, upperRegionGreen)
        edgesGreen = cv2.Canny(ObjectGreen, 100, 200)
        # cv2.imshow("Edges", edgesOrange)
        contoursGreen, _ = cv2.findContours(edgesGreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        detectionsGreen = []
        for cnt in contoursGreen:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > 1500:
                print(area)
                cv2.drawContours(hsv, [cnt], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)

                detectionsGreen.append([x, y, w, h])

                # 2. Object Tracking
                boxes_ids = tracker.tracking_update(detectionsGreen)
                for box_id in boxes_ids:
                    x, y, w, h, id = box_id
                    cv2.putText(roi, "Green id:" + str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    print("Number of Green pieces: " + str(id + 1))
                    numberGreen = id + 1
                
                
                
                
                
                
    cv2.imshow("roi", roi)
    cv2.imshow("Frame", frame)
    # cv2.imshow("Mask", mask)

    f = open("Demo.txt", "w")

    f.writelines("Orange pieces: "+str(numberOrange))
    f.writelines('\n')
    f.writelines("Yellow pieces: "+str(numberYellow))
    f.writelines('\n')
    f.writelines("Green pieces: "+str(numberGreen))
    f.writelines('\n')
    f.close()


    key = cv2.waitKey(30)
    if key == 27:
        break
        
camera.stop_recording()
camera.close()
# cap.release()
cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

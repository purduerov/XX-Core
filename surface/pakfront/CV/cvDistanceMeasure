#!/usr/bin/env  python
import subprocess
import io
import cv2
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
from CVhandles import get_image, pushframe, pushdata
from multiprocessing import Process, Pool
import time
from UndistortFisheye import *
signal(SIGPIPE, SIG_DFL)


def calcDistances(imgColor):
    # undistort image using calibration
    imgColor = undistortFisheye(imgColor)
    # convert to HSV
    img = cv2.cvtColor(imgColor, cv2.COLOR_BGR2HSV)
    # thresholds (H: 0->180 (2* degree in normal HSV),
    # S: 0->255 (scaled up from 0-100),
    # V:0->255 (scaled up from 0-100))
    # These thresholds may need to change when we change 
    # locations, found to work well with test data
    redThresh = ((52,0,0),(180, 255, 158))
    yellowThresh = ((24,69,154),(79,255,255))
    #blueThresh =((21,53,76), (44,255,255))
    #greenThresh = ((40,40,25), (90, 255, 255))
    threshes = (redThresh, yellowThresh)#, blueThresh, greenThresh)


    # kernel for dilate and erode
    kern = np.ones((5,5))*5
    img2 = None
    # apply thresholds and blur to get binary image holding 
    # brightly colored parts (the square and marks)
    for thresh in threshes:
        temp = cv2.inRange(img, *thresh)
        temp = cv2.dilate(temp, kern)
        temp = cv2.erode(temp, kern)
        temp = cv2.GaussianBlur(temp, (5,5),0)
        if img2 is not None:
            img2 += temp
        else:
            img2 = temp


    # get contours
    _,contours,_ = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Locate the largest countor that is square-sized
    #  - should be the square
    # if all 4 sides are visible in undistorted image
    maxArea = 0
    square  = []
    for c in contours:
        area = cv2.contourArea(c)
        if (area > maxArea) and (area < 200 * 200):
            maxArea = area
            square = c

    # if no contour is found meeting the criteria, return
    if square == []:
        return imgColor, {"start" : [], "points": [], "sideLength": None}
    
    # reduce the found contour to a square
    square = cv2.approxPolyDP(square, 30, True) # Well that was easy
    
    # check for 4 points here
    if len(square) != 4:
        return imgColor, {"start" : [], "points": [], "sideLength": None}

    # overlay the square on the image
    cv2.drawContours(imgColor, [np.array(square)], 0, (255,0,0), 5)

    # find the colored marks on the PVC

    # start by filtering out contours too big or small
    coloredMarks = []
    for c in contours:
        # calculate the area of the contour
        area = cv2.contourArea(c)
        # the area of the marks is less than the square's area
        # and greater than minSize (here 30)
        if area < maxArea/10 and area > 30:
            # calculate and save the centroid of each contour
            # cv2.drawContours(imgColor,[c],0,(0,255,0), 5)
            sumx = np.sum(c[:,:,0])
            sumy = np.sum(c[:,:,1])
            coloredMarks.append((int(sumx/len(c)),int(sumy/len(c))))        

    # function to determine if 3 points are collinear
    # 3000 determined to indicate "collinear enough"
    def collinear(p0,p1,p2):
        x1,y1 = p1[0] - p0[0], p1[1] - p0[1]
        x2,y2 = p2[0] - p0[0], p2[1] - p0[1]
        collineararity = x1 * y2 - x2 * y1
        return abs(collineararity) < 3000

    # find the side of the square that is collinear
    # with the most colored marks 
    # only save the points that are in the largest 
    # set of collinear points 

    finalMarks = []
    maxCnt = 0
    start = ()
    sideLength = 0
    for i in range(len(square)):
        corner1 = list(square[i][0])
        corner2 = list(square[i-1][0])
        collinearCnt = 0
        goodPoints = []
        for mark in coloredMarks:
            if collinear(corner1,corner2,mark):
                collinearCnt += 1
                goodPoints.append(mark)
        if collinearCnt > maxCnt:
            maxCnt = collinearCnt
            finalMarks = goodPoints
            start = corner1
            sideLength = l2Norm(corner2, corner1)

    # pack the start point and locations of colored marks
    # to send out
    distanceData = {"start": start, "points": finalMarks, "sideLength": sideLength}

    return imgColor, distanceData

# TEST MEASUREMENTS
# yellow 27 cm (67 cm) 49
# red 49.53 cm  (90 cm) 63
# blue 77.47 cm  (117 cm) 80
# green 86.06 (126 cm)

# function converts pixel distances to cm distances
def pix2cm(pixDist, sideLength=None):
    if sideLength:
        return pixDist * (40/sideLength)
    else:
        return pixDist * (40/200) * (1.43)

# calculate the eculidean distance between 2 points
def l2Norm(p1,p2):
    return np.linalg.norm((p2[0] - p1[0], p2[1] - p1[1]))

#  Draw the distances of the found points
def drawDists(start, filteredPoints, imgColor, sideLength=None):
    # calculate distances in cm, display on image
    distanceList = []
    if start:
        font = cv2.FONT_HERSHEY_SIMPLEX
        offset = 8 # offset from edge of square to measurement point
        cv2.putText(imgColor,str(0.0), tuple(start), font, 0.75,(0,0,255),2,cv2.LINE_AA)
        for point in filteredPoints:
            d = pix2cm(l2Norm(start, point),sideLength)
            distanceList.append(d)
            cv2.putText(imgColor,str(round(d,1) + offset), point, font, 0.75,(0,0,255),2,cv2.LINE_AA)
    return imgColor, distanceList



if __name__ == '__main__': 
# Load in RGB image, find distances

    i = 0
    filteredPoints = {}
    # the following parameters have been found to work
    # with test camera data, may have to change with a
    # new camera or pool

    thresh = 15 # for minimum distance between points
    maxCnt = 25 # higest a count will go for a point
    minCnt = 5  # minimum count for a point to be displayed
    while True:
        # read video stream
        frame = get_image(0) # may need to change this to correct camera
        # do the distance caclulation
        imgColor, data = calcDistances(frame)
        # decay points not found
        for x,cnt in filteredPoints.items():
            if cnt > 0:
                filteredPoints[x] -= 1
        # compare new points to existing
        # if within thresh
        #  increment value for existing point
        # if not matching any point
        #  add to list with value 0
        for p in data["points"]:
            done = 0
            for x,cnt in filteredPoints.items():
                if l2Norm(x,p) < thresh and not done:
                    if cnt < maxCnt:
                        filteredPoints[x] += 2
                    else:
                        filteredPoints[x] += 1
                    done = 1
                    break
            if not done:
                filteredPoints[p] = 0

        # filter out under a certain count
        drawPoints = [x for x,cnt in filteredPoints.items() if cnt > minCnt]
        # Draw the filtered points
        imgColor, retData = drawDists(data["start"], drawPoints, imgColor, data["sideLength"])
        # return image and data
        
        retData.sort()
        # retdata is simply a dictionary with one element:
        # 'Distances', which is an array containing the distances in cm
        # of the colored marks, sorted in acending order
        retData = {"Distances" : retData}
        pushframe(imgColor, 3) # May need to change these ID's
        pushdata(retData, 3) 
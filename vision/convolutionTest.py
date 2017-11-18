import cv2
from settings import *
import numpy as np
import copy
from imageProc import findScale, adjustScale

#Assumes Opencv3.0 and python 3.6 through Anaconda

# Parameters assumed to be defined in settings.py
# The user must define a Settings.py file
# This is not commited so we can maintain different parameters
# After -- is example definition
#================================================
# videoFilename -- "../calib1.mp4"
# vidStartTime  --  31
# vidStopTime  --   41
# templateFilename -- "template.png"
# calibFilename -- "calib.json"
#================================================


# Create video feed
cap = cv2.VideoCapture(videoFilename)
# create and resize named window to view stream
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 640, 480)

# load template image
templates = []

template = cv2.imread(templateFilename, cv2.IMREAD_COLOR)

#Generate an array of templates of varying sizes
#Generate correlation factors for each template
for scale in np.arange(.1, 1, .1):
    tmp = cv2.resize(template, (int(scale * template.shape[0]), int(scale * template.shape[1])),
                     interpolation=cv2.INTER_CUBIC)
    tmp1 = tmp.copy()
    res = cv2.matchTemplate(tmp, tmp1, cv2.TM_SQDIFF)
    _, maxVal, _, _ = cv2.minMaxLoc(res)
    templates.append((tmp.copy(), maxVal))


# set feed start time
frameNum = vidStartTime
isFrameLost = True
currFrameIndex = 0

while cap.isOpened():
    ret, frame = cap.read()

    if isFrameLost:
      currFrameIndex = findScale(frame, templates)
      isFrameLost = False

    print(currFrameIndex)
    topLeft, currFrameIndex = adjustScale(frame, currFrameIndex, templates)
    bottomRight = (topLeft[0] + templates[currFrameIndex][0].shape[0],
                   topLeft[1] + templates[currFrameIndex][0].shape[1])
    cv2.rectangle(frame, topLeft, bottomRight, (0,255, 0), 5, 8, 0)
    frameNum += 1



    """
    #Locate object in frame
    res = cv2.matchTemplate(frame, template, cv2.TM_CCORR_NORMED)
    cv2.normalize(res, res, 0, 1, cv2.NORM_MINMAX, -1)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    topLeft = maxLoc
    bottomRight = (topLeft[0] + w, topLeft[1] + h)
    """

    #Display result
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# Don't be a piggy, clean up!
cap.release()
cv2.destroyAllWindows()

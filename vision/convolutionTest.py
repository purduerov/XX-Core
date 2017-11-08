import cv2
from settings import *

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
template = cv2.imread(templateFilename, cv2.IMREAD_COLOR)
h, w = template.shape[0], template.shape[1]
# stream is upside down for some reason, so I flip the template
M = cv2.getRotationMatrix2D((w/2, h/2), 180, 1)
template = cv2.warpAffine(template, M, (w, h))
# need to scale the template, shouldn't need this once we have gaussian pyramid
template = cv2.resize(template, (int(2 * w), int(2 * h)), interpolation=cv2.INTER_CUBIC)
h, w = template.shape[0], template.shape[1]
# set feed start time
cap.set(1, vidStartTime)
while(cap.isOpened()):
    ret, frame = cap.read()

    #Generate Gaussian Pyramid



    #Locate object in frame
    res = cv2.matchTemplate(frame, template, cv2.TM_CCORR_NORMED)
    cv2.normalize(res, res, 0, 1, cv2.NORM_MINMAX, -1)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    topLeft = maxLoc
    bottomRight = (topLeft[0] + w, topLeft[1] + h)

    cv2.rectangle(frame, topLeft, bottomRight, (0, 255, 0), 5, 8, 0)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Display result
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# Don't be a piggy, clean up!
cap.release()
cv2.destroyAllWindows()

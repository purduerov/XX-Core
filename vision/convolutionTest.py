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
#================================================


# Create video feed
cap = cv2.VideoCapture(videoFilename)
while(cap.isOpened()):
    ret, frame = cap.read()

	#Generate Gaussian Pyramid



	#Locate object in frame


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#Display result
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# Don't be a piggy, clean up!
cap.release()
cv2.destroyAllWindows()

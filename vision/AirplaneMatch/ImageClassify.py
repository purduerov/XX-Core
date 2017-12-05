import cv2
import numpy as np

filename = "assets/yellowTriangle.png"
redThresh = ((0,127,122),(4, 250, 180))
yellowThresh =((25,40,50), (30,255,255))
blueThresh = ((105,50,25),(120,255,255))
threshes = (redThresh, yellowThresh, blueThresh)

# Load in RGB image
img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2HSV)
imgColor = cv2.imread(filename)

#Holds a contour for each color threshold
all_contours = []

for thresh in threshes:
    img2 = cv2.inRange(img,*thresh)
    kern = np.ones((3,3))*3 # Maybe erode this to remove point noise
    img2 = cv2.dilate(img2, kern)
    img2 = cv2.medianBlur(img2, 5)
    _,contours,_ = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        all_contours.append([])
        continue

    #TODO check if it is a rectangle or a triangle
    c = max(contours, key=cv2.contourArea)
    all_contours.append(c)


# Locate the largest contour and ID its color
maxArea =0
index = -1
for i,c in enumerate(all_contours):
    if len(c) > 0:
        area = cv2.contourArea(c)
        if area > maxArea:
            maxArea = area
            index = i

c = np.array(all_contours[index])
shape = cv2.approxPolyDP(c, 10, True) # Well that was easy
colors = ((0,0,255), (0,255,255), (255,0,0))
color_names = ("Red_Rect", "Yellow_Rect", "Blue_Rect", "Red_Triangle", "Yellow_Triangle", "Blue_Triangle")
shapes = ("Rect", "Triangle")

cv2.drawContours(imgColor, [np.array(shape)], 0, colors[index], 5)
cv2.imshow(color_names[index+3] if len(shape) == 3 else color_names[index], imgColor)
cv2.waitKey()
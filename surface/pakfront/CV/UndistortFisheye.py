import numpy as np
import cv2
import json


# Takes an openCV image, img and performs 
# fisheye unidistortion using the calibration
# stored in calib.json

def undistortFisheye(img):
    with open("calib.json","r") as f:
        calib = json.load(f)
    K = np.array(calib["K"])
    D = np.array(calib["D"])
    m1, m2 = cv2.fisheye.initUndistortRectifyMap(K,D,np.eye(3),K,img.shape[:2][::-1],cv2.CV_16SC2)
    undistortedImg = cv2.remap(img,m1,m2,interpolation=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
    return undistortedImg

if __name__ == '__main__':
    img = cv2.imread("calib4095.jpg")
    undistortedImg = undistortFisheye(img)
    compare = np.hstack((img,undistortedImg))
    cv2.imshow("undistort",compare)
    cv2.waitKey()
    cv2.imwrite("calib4095_undistort.jpg", undistortedImg)
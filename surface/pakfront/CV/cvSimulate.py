#!/usr/bin/env  python
import subprocess
import io
import cv2
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
from CVhandles import get_image, pushframe, pushdata
from multiprocessing import Process, Pool
import time
signal(SIGPIPE, SIG_DFL)

if __name__ == "__main__":
    curimage = cv2.imread("/home/zhukov/testimage.jpg")
    while True:
        #curimage = get_image(0)
        data = {"Foo":"https://i.pinimg.com/originals/00/21/52/002152ecac89b72d602059193ebdc161.jpg"}
        time.sleep(0.1)
        # CV stuff goes here
        pushframe(curimage,1)
        pushdata(data,1)

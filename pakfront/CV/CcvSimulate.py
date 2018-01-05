#!/usr/bin/env  python
import subprocess
import io
import cv2
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
from CVhandles import get_image, pushframe
from multiprocessing import Process, Pool
import time
signal(SIGPIPE, SIG_DFL)

if __name__ == "__main__":
    while True:
        curimage = get_image(1917, 0)
        time.sleep(0.001)
        grayimg = cv2.cvtColor(curimage, cv2.COLOR_BGR2GRAY)
        # CV stuff goes here
        pushframe(grayimg)

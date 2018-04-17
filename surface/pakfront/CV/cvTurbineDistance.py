#!/usr/bin/env  python
# Return Structure {Distances: int[]}
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
    while True:
        # load rgb image
        curimage = get_image(0)
        data = {"Distances": [41,42,43,44,45]}
        pushframe(curimage,3)
        pushdata(data,3)

import subprocess
import time
import io
import cv2
import numpy as np
import requests as r
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

def getframe():
    imreq = subprocess.check_output(["./socket"])
    raw = io.BytesIO(imreq)
    data = np.fromstring(raw.getvalue(),dtype = np.uint8)
    return cv2.imdecode(data,1)

def pushframe(img):
    postdata = cv2.imencode(".jpg",img)
    imdata = bytearray([b[0] for b in postdata[1]])
    lenbytes = bytearray.fromhex('{:08x}'.format(len(imdata)))

    writeimage(imdata)

    imreq = subprocess.Popen(["./stintotcp","1918"],stdin=subprocess.PIPE)
    imreq.stdin.write(bytearray([0 for i in range(0,5 - len(lenbytes))]))
    imreq.stdin.write(lenbytes)
    imreq.stdin.write(imdata)
    imreq.stdin.close()
    return len(imdata)

def writeimage(data):
    with open("im.jpg","wb+") as fh:
        fh.write(data)

if __name__ == "__main__":
    image = getframe()
    # CV stuff goes here
    print(pushframe(image))

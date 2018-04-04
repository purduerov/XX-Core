import subprocess
import io
import cv2
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
from multiprocessing import Process, Pool
from json import dumps
import time
signal(SIGPIPE, SIG_DFL)
MJPGPORT=8080
ROVIP="localhost"


def get_image(camnum):
    port = MJPGPORT
    imreq = subprocess.check_output(["tcptostdin",str(MJPGPORT),str(camnum),ROVIP])
    raw = io.BytesIO(imreq)
    data = np.fromstring(raw.getvalue(), dtype=np.uint8)
    return cv2.imdecode(data, 1)


def getframe(port,camnum):
    pool = Pool(processes=1)
    p = pool.apply_async(get_image)
    pool.close()
    return p


def pushframe(image,ID):
    port = 4*ID + 3 + 1917
    def push(img):
        postdata = cv2.imencode(".jpg", img)
        imdata = bytearray([b[0] for b in postdata[1]])
        lenbytes = bytearray.fromhex('{:08x}'.format(len(imdata)))
        imreq = subprocess.Popen(["stintotcp", str(port)], stdin=subprocess.PIPE)
        imreq.stdin.write(bytearray(8 - len(lenbytes)))
        imreq.stdin.write(lenbytes)
        imreq.stdin.write(imdata)
        imreq.stdin.close()
        return len(imdata)
    p = Process(target=push, args=(image,))
    p.start()
    return "Push Initiated"

def pushdata(data, ID):
    port = 4*ID + 4 + 1917
    def push(da, port):
        data = bytearray()
        d = dumps(da)
        data.extend(d)
        lenbytes = bytearray.fromhex('{:08x}'.format(len(data)))
        imreq = subprocess.Popen(["stintotcp", str(port)], stdin=subprocess.PIPE)
        imreq.stdin.write(bytearray(8 - len(lenbytes)))
        imreq.stdin.write(lenbytes)
        imreq.stdin.write(data)
        imreq.stdin.close()
        return len(data)
    p = Process(target=push, args=(data,port))
    p.start()
    return "Push Initiated"

def writeimage(name,data):
    with open("/home/zhukov/Projects/rov/test/" + name, "wb+") as fh:
        fh.write(data)


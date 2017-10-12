import promise
import subprocess
import io
import cv2
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
from multiprocessing import Process
signal(SIGPIPE, SIG_DFL)


def getframe():
    def get():
        imreq = subprocess.check_output(["./tcptostdin"])
        raw = io.BytesIO(imreq)
        data = np.fromstring(raw.getvalue(), dtype=np.uint8)
        return cv2.imdecode(data, 1)
    return promise.promisify(get)


def pushframe(image):
    def push(img):
        postdata = cv2.imencode(".jpg", img)
        imdata = bytearray([b[0] for b in postdata[1]])
        lenbytes = bytearray.fromhex('{:08x}'.format(len(imdata)))
        imreq = subprocess.Popen(["./stintotcp", "1918"], stdin=subprocess.PIPE)
        imreq.stdin.write(bytearray(5 - len(lenbytes)))
        imreq.stdin.write(lenbytes)
        imreq.stdin.write(imdata)
        imreq.stdin.close()
        return len(imdata)
    Process(target=push, args=image).start()


def writeimage(data):
    with open("im.jpg", "wb+") as fh:
        fh.write(data)

if __name__ == "__main__":
    curimage = getframe()
    # CV stuff goes here
    print(pushframe(curimage))

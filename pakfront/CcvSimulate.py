import subprocess
import io
import cv2
import numpy as np
from signal import signal, SIGPIPE, SIG_DFL
from multiprocessing import Process, Pool
signal(SIGPIPE, SIG_DFL)


def get_image():
    imreq = subprocess.check_output(["./tcptostdin"])
    raw = io.BytesIO(imreq)
    data = np.fromstring(raw.getvalue(), dtype=np.uint8)
    return cv2.imdecode(data, 1)


def getframe():
    pool = Pool(processes=1)
    p = pool.apply_async(get_image)
    pool.close()
    return p


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
    p = Process(target=push, args=(image,))
    p.start()
    return "Push Initiated"


def writeimage(data):
    with open("im.jpg", "wb+") as fh:
        fh.write(data)


if __name__ == "__main__":
    curimage = getframe()
    # CV stuff goes here
    print(pushframe(curimage.get()))

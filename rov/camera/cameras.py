import subprocess
import os
import time
import signal
from camera import Camera

DEVNULL = open(os.devnull, 'w')

class Cameras(object):

    def __init__(self, resolution='1280x720', framerate=30,
                 devices=None, port=8080, brightness=16, contrast=32):
        """
        Initializes the camera object and determines the cameras in the dev file to use.
        """
        self.process = None
        self.resolution = resolution
        self.framerate = framerate
        self.port = port
        self.cameras =[]
        self.output = 'output_http.so -p {port} {web}'.format(
            port=port,
            web='-w /usr/local/www'
        )

        # sometimes there will be video devices in dev that dont work this is to check those and not include them in the list of active cameras.
        if not devices:
            devs = ['/dev/' + dev for dev in os.listdir('/dev') if dev.startswith('video')]
            self.devices = []

            # attempt to run a specfic camera to see if it works.
            temp = {}
            # variable to change the port
            x = 1
            for dev in devs:
                tempin = 'input_uvc.so -r {resolution} -d {device}'.format( resolution=self.resolution, device=dev)
                try:
                    output = 'output_http.so -p {port} {web}'.format(
                        port=port+x,
                        web='-w /usr/local/www'
                    )
                    temp.update({dev: subprocess.Popen(['mjpg_streamer', '-i', tempin, '-o', output], stdout=DEVNULL, stderr=DEVNULL)})
                    x+=1
                except Exception:
                    pass
            # let them get set up then check
            time.sleep(0.05)
            for k, v in temp.items():
                if v.poll() is None:
                    v.kill()
                    self.devices.append(k)
        else:
            self.devices = devices

        self.brightness = brightness
        self.contrast = contrast
        self.input = ['input_uvc.so -r {resolution} -d {device}'.format( resolution=self.resolution, device=d) for d in self.devices]
        self.status = 'killed'
        for camnum, dev in enumerate(self.devices):
            cam = Camera(
                        resolution=self.resolution,
                        framerate=self.framerate,
                        device=dev,
                        port=self.port + camnum,
                        brightness=self.brightness,
                        contrast=self.contrast
            )
            self.cameras.append(cam)

    def start(self):
        for cam in self.cameras:
            time.sleep(0.2)
            cam.start()
        return self

    def kill(self):
        for cam in self.cameras:
            cam.kill()
        self.system_kill()

    def system_kill(self):
        os.system("pgrep 'mjpg' | xargs kill -9")

    def status(self):
        return {
        'Cam_' + str(cam.port - self.port): {'port': cam.port, 'status': cam.get_status()}
        for cam in self.cameras
        }

    def set_status(self,status):
        print("setting status")
        for index, state in enumerate(status):
            for cam in self.cameras:
                print("setting status for cam {}".format(cam.port))
                if cam.port-self.port == index:
                    if state:
                        cam.unsuspend()
                    else:
                        cam.suspend()

if __name__ == '__main__':
    cam = Cameras().start()
    time.sleep(2)
    print "Cameras Running"
    print "To access Cameras go into your browser and go to"
    print "<ip of rov>:{}/?action=stream_<camnumber>".format(cam.port)
    raw_input("to kill cameras press enter")
    cam.stop()


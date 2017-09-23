import os
import signal
import subprocess


class Camera(object):

    # In order to run mjpg-streamer through Python, make sure
    # mjpg-streamer-experimental is installed so the .so objects
    # and mjpg-streamer are all on defualt PATH so we don't have
    # to specify path (was getting a lot of errors resulting from
    # files not being able to be found. Resolution must also be
    # specified in "integerxinteger" and not by name.

    # default layout for camera
    def __init__(self, resolution='1280x720', framerate=30, device='/dev/video0', port=8080, brightness=16, contrast=32):
        self.process = None
        self.resolution = resolution
        self.framerate = framerate
        self.device = device
        self.port = port
        self.brightness = brightness
        self.contrast = contrast

        self.input = 'input_uvc.so -d {device}'.format(
            device=self.device,
        )
        self.output = 'output_http.so -p {port} {web}'.format(
            port=self.port,
            web='-w /usr/local/www'
        )

        self.status = "killed"

    # framerate shouldn't be changed: keep at 30, allows for a good image while
    # reserving valuable processing power for other devices. Device is formatted as a
    # string: /dev/videoNUM where NUM is the number for the order in which camera is
    # plugged in, starting at 0. Port is the web port where you want to output image
    # to: change as needed

    # open video feed for an instance of Camera
    def start(self):
        self.process = subprocess.Popen(['mjpg_streamer', '-i', self.input, '-o', self.output])

        if self.is_alive():
            self.status = 'active'

    # closes video feed for an instance of Camera: each instance of Camera must be killed
    # using this method
    def kill(self):
        if self.is_alive():
            self.process.kill()
            self.status = 'killed'

    def suspend(self):
        os.kill(self.process.pid, signal.SIGSTOP)
        self.status = 'suspended'

    def unsuspend(self):
        if self.status == 'suspended':
            os.kill(self.process.pid, signal.SIGCONT)
            self.status = 'active'

    def is_alive(self):
        if self.process is None:
            return False
        return (self.process.poll() is None)

    def get_status(self):
        if not self.is_alive():
            self.status = 'killed'

        return self.status

    def set_status(self, status):
        if status == 'active':
            if self.status == 'suspended':
                self.unsuspend()
            elif self.status == 'killed':
                self.start()
        elif status == 'suspended':
            if self.status == 'active':
                self.suspend()
        elif status == 'killed':
            self.kill()

import subprocess
import os
import time

DEVNULL = open(os.devnull, 'w')

class Cameras(object):

    def __init__(self, resolution='1280x720', framerate=30,
                 devices=None, port=8080, brightness=16, contrast=32):
        self.process = None
        self.resolution = resolution
        self.framerate = framerate
        self.port = port
        self.output = 'output_http.so -p {port} {web}'.format(
            port=port,
            web='-w /usr/local/www'
        )
        if not devices:
            devs = list(subprocess.check_output('ls /dev/video*', shell=True).splitlines())
            self.devices = []
            for dev in devs:
                tempin = 'input_uvc.so -f {framerate} -r {resolution} -d {device}'.format(framerate=self.framerate, resolution=self.resolution, device=dev)
                try:
                    temp = subprocess.Popen(['mjpg_streamer', '-i', tempin, '-o', self.output], stdout=DEVNULL, stderr=DEVNULL)
                    time.sleep(0.5)
                    if temp.poll() is None:
                        temp.kill()
                        self.devices.append(dev)
                except Exception:
                    pass
        else:
            self.devices = devices
        self.brightness = brightness
        self.contrast = contrast
        self.input = ['input_uvc.so -f {framerate} -r {resolution} -d {device}'.format(framerate=self.framerate, resolution=self.resolution, device=d) for d in self.devices]

    def start(self):
        command = ['mjpg_streamer']
        for i in self.input:
            command.append('-i')
            command.append(i)
        command.append('-o')
        command.append(self.output)
        print command
        self.process = subprocess.Popen(command, stdout=DEVNULL, stderr=DEVNULL)

if __name__ == '__main__':
    print Cameras().start()

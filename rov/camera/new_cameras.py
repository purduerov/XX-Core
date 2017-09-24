import subprocess


class Cameras(object):

    def __init__(self, resolution='1280x720', framerate=30,
                 devices=None, port=8080, brightness=16, contrast=32):
        self.process = None
        self.resolution = resolution
        self.framerate = framerate
        if not devices:
            self.devices = list(subprocess.check_output('ls /dev/video*', shell=True).splitlines())
        else:
            self.devices = devices
        self.port = port
        self.brightness = brightness
        self.contrast = contrast
        self.input = ['input_uvc.so -d {device}'.format(device=d) for d in self.devices]
        self.output = 'output_http.so -p {port} {web}'.format(
            port=port,
            web='-w /usr/local/www'
        )

    def start(self):
        command = ['mjpg_streamer']
        for i in self.input:
            command.append('-i')
            command.append(i)
        command.append('-o')
        command.append(self.output)
        print command
        self.process = subprocess.Popen(command)

if __name__ == '__main__':
    print Cameras().start()

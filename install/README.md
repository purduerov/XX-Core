# X9-Core
All of X9's core software for the 2016-2017 Purdue ROV team.

### To install Python and Flask app:
1. install core packages and dependencies:
`sudo apt-get install gcc python python-dev python-pip python-smbus libffi-dev`

2. install virtualenv
`sudo pip install virtualenv`

3. create new virtualenv to manage python packages (creates folder 'venv'):
`virtualenv venv`

4. activate virtual environment:
`. venv/bin/activate`

5. install python packages:
`pip install -r requirements.txt`

6. apply sudo to pip installation if any fail due to permissions

7. make sure all packages are installed and flask runs with:
`export FLASK_APP=application.py`
`flask run --host=0.0.0.0`

8. stop using virtual environment with:
`deactivate`

### To install mjpg-streamer:
1. install dependencies with
`sudo apt-get install libjpeg8-dev imagemagick libv4l-dev cmake`

2. create symbolic link of video.h with
`sudo ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h`

3. inside mjpg-streamer run
`sudo make`
`sudo make install`

4. create environment variable to installed .so files (could insert it into .bashrc):
`export LD_LIBRARY_PATH=/usr/local/lib/`

5. If problems persist, make .so files in /usr/local/lib have all permissions:
`sudo chmod 777 /usr/local/lib/mjpg-streamer -R`

6. Stick an iframe in html:
```
<iframe src="http://10.42.0.?:8080/?action=stream" width="1024" height="768" scrolling="no" frameborder="no" marginheight="0px" position"absolute" css="right=0; top=0;"></iframe>
```

### To install i2c for Pi:
1. install dependencies with
 `sudo apt-get install python-smbus i2c-tools`

2. Configure i2c with raspi-config:
 `sudo rasp-config` > Advanced Options > I2C

3. reboot Pi with:
 `sudo reboot`

4. test with (should print out i2c addresses of devices attached to the i2c line):
 `i2cdetect -y 1`

### To install node and Vue:
1. it looks like npm needs a library provided by adafruit, so run: `curl -sLS https://apt.adafruit.com/add | sudo bash`

2. The vue we're using is a node module, so just run: `sudo apt-get install nodejs npm`

3. now, navigate to `X9-Core/frontend/` and run `npm install`

4. once that's done, just run `npm run build` to condense the files for the webpage

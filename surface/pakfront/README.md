# Pakfront
Proxy that routes traffic between the frontend and ROV. Logs shit, passes image data to CV

![picture alt](https://i.pinimg.com/736x/1a/e4/8f/1ae48fbbbe08af14ea305fe71fd4dae5--battle-of-monte-cassino-machine-guns.jpg)
## Pakfront and Running it: What does it do? How do you install it? Let's find out
Pakfront is written in Go, which is a compiled language, like C, but they build system is way less convoluted. For our purposes, the final product we are looking for is a binary which can be run like any other executable(it also needs a config file, but that just sits in surface), and some python scripts that can be run as CV subprocesses. This all sits in the pakfront/bin/ directory, which one can run at his or her own leisure.

### Installation
(To Be updated in proxy_install branch)

### Launching
Once everything has been installed, you can launch "panzerkanone", which is located in the pakfront bin. 
Some requirements to run it.
* Make sure you have a proxyconfig file in the directory you run in from, so in surface should be fine. 
* The config file should be pointing to a running flask socket-io instance, whether it be localhost or a pi. Be sure to check.
* Set the enviroment variable LOGDIR to where you want to save the log file. It will default to cwd. You can do so with,

`export LOGDIR=<your log directory here>`

If running on a dev machine, it is recommended you modify your .profile or .bashrc to have a global log directory.
Launch pakfront and all the CV processes like you would anything,

` ./anything `

pakfront needs to be running in order to interface with CV processes

### Interfacing
Pakfront communicates through a series of ports. It's hard to keep track of sometimes, so to find which process is running simply make a GET request to localhost:1905. The JSON returned should tell you everything you need to know about interfacing with pakfront. It tells you which socketio port to request through in order to log things, what cv processes are accessable, and what those processes data and stream ports are.


## Why is it named pakfront
Because how else will we drive back the invader?

https://en.wikipedia.org/wiki/Pakfront

#!/bin/bash
mjpg_streamer -i 'input_uvc.so -d /dev/video1'  -o 'output_http.so -p 8080 -w /usr/local/www'

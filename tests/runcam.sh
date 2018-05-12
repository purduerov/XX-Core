#!/bin/bash
mjpg_streamer  -i 'input_uvc.so -d /dev/video0' -i 'input_uvc.so -d /dev/video1' -i 'input_uvc.so -d /dev/video3'  -o 'output_http.so -p 8080 -w /usr/local/www'

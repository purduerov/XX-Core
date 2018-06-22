gst-launch-1.0 -v v4l2src device=/dev/video0 ! "image/jpeg,width=1280, height=720, framerate=30/1" ! rtpjpegpay ! udpsink host=0.0.0.0 port=8080 &
gst-launch-1.0 -v v4l2src device=/dev/video1 ! "image/jpeg,width=1280, height=720, framerate=30/1" ! rtpjpegpay ! udpsink host=0.0.0.0 port=8080 &
gst-launch-1.0 -v v4l2src device=/dev/video2 ! "image/jpeg,width=1280, height=720, framerate=30/1" ! rtpjpegpay ! udpsink host=0.0.0.0 port=8080 &
gst-launch-1.0 -v v4l2src device=/dev/video3 ! "image/jpeg,width=1280, height=720, framerate=30/1" ! rtpjpegpay ! udpsink host=0.0.0.0 port=8080 &
gst-launch-1.0 -v v4l2src device=/dev/video4 ! "image/jpeg,width=1280, height=720, framerate=30/1" ! rtpjpegpay ! udpsink host=0.0.0.0 port=8080 &

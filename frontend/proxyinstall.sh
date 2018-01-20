#!/bin/bash
pxydir="../pakfront"
sudo apt-get install -y golang 
go get github.com/graarh/golang-socketio
go get github.com/googollee/go-socket.io
go build $pxydir/stintotcp.go 
go build $pxydir/tcptostdin.go 
go build $pxydir/pakfront.go $pxydir/imgbuffer.go $pxydir/sockiopxy.go $pxydir/CVdata.go $pxydir/transparent.go $pxydir/logger.go
mv stintotcp bin/
mv tcptostdin bin/
mv pakfront bin/
cp $pxydir/CV/* bin/
cp $pxydir/proxyconfig.json .
cp $pxydir/CVhandles.py bin/

#!/bin/bash
pxydir="pakfront"
outname="panzerkanone"
sudo apt-get install -y golang 
go get github.com/graarh/golang-socketio
go get github.com/googollee/go-socket.io
go build $pxydir/stintotcp.go 
go build $pxydir/tcptostdin.go 
go build -o $outname $pxydir/pakfront.go $pxydir/imgbuffer.go $pxydir/sockiopxy.go $pxydir/CVdata.go $pxydir/transparent.go $pxydir/logger.go
mv stintotcp pakfront/bin/
mv tcptostdin pakfront/bin/
mv $outname pakfront/bin/
cp $pxydir/* pakfront/bin/
cp $pxydir/proxyconfig.json pakfront/.
cp $pxydir/CVhandles.py pakfront/bin/
sudo chmod -R 770 pakfront/bin/*

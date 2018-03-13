#!/bin/bash
pxydir="pakfront"
outname="panzerkanone"
sudo apt-get install -y golang 
CWD="$(pwd)"
PROF="$(tail -n 1 ~/.profile)"
if [[ $PROF != *"GOPATH"* ]]; then
        echo "Updating Profile"
        echo "export GOPATH=${CWD}/pakfront/" >> ~/.profile
        source ~/.profile
fi
go get github.com/graarh/golang-socketio
go get github.com/googollee/go-socket.io
go build $pxydir/stintotcp.go 
go build $pxydir/tcptostdin.go 
go build -o $outname $pxydir/pakfront.go $pxydir/imgbuffer.go $pxydir/sockiopxy.go $pxydir/CVdata.go $pxydir/transparent.go $pxydir/logger.go
mv stintotcp $pxydir/bin/
mv tcptostdin $pxydir/bin/
mv $outname $pxydir/bin/
cp $pxydir/CV/* $pxydir/bin/
cp $pxydir/proxyconfig.json .
cp $pxydir/CVhandles.py $pxydir/bin/
sudo chmod -R 770 $pxydir/bin/*

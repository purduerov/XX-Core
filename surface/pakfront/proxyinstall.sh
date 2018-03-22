#!/bin/bash
pxydir="pakfront"
outname="panzerkanone"
sudo apt-get install -y golang 
pip install opencv-python
CWD="$(pwd)"
PROF="$(tail -n 2 ~/.profile)"
if [[ $PROF != *"GOPATH"* ]]; then
        echo "Updating Profile"
        echo "export GOPATH=${CWD}/pakfront/" >> ~/.profile
fi
if [[ $PROF != *"/pakfront/bin"* ]]; then
        echo "Updating Profile"
        echo "export PATH=\"\$PATH:${CWD}/pakfront/bin\"" >> ~/.profile
fi
source ~/.profile
go get github.com/graarh/golang-socketio
go get github.com/googollee/go-socket.io
go build $pxydir/stintotcp.go 
go build $pxydir/tcptostdin.go 
go build -o $outname $pxydir/pakfront.go $pxydir/imgbuffer.go $pxydir/sockiopxy.go $pxydir/CVdata.go $pxydir/transparent.go $pxydir/logger.go
mv stintotcp $pxydir/bin/
mv tcptostdin $pxydir/bin/
mv $outname $pxydir/bin/
cp $pxydir/CV/* $pxydir/bin/
cp $pxydir/CVhandles.py $pxydir/bin/
sudo chmod -R 770 $pxydir/bin/*

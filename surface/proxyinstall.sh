#!/bin/bash
pxydir="pakfront"
outname="panzerkanone"
sudo apt-get install -y golang 
go get github.com/graarh/golang-socketio
go get github.com/googollee/go-socket.io
go build $pxydir/stintotcp.go 
go build $pxydir/tcptostdin.go 
go build -o $outname $pxydir/pakfront.go $pxydir/imgbuffer.go $pxydir/sockiopxy.go $pxydir/CVdata.go $pxydir/transparent.go $pxydir/logger.go
<<<<<<< HEAD
mv stintotcp $pxydir/bin/
mv tcptostdin $pxydir/bin/
mv $outname $pxydir/bin/
# cp -r $pxydir/* bin/
# cp -r $pxydir/proxyconfig.json .
cp -r $pxydir/CV $pxydir/bin/
sudo chmod -R 770 $pxydir/bin/*
=======
mv stintotcp bin/
mv tcptostdin bin/
mv $outname bin/
cp $pxydir/CV/* bin/
cp $pxydir/proxyconfig.json .
cp $pxydir/CVhandles.py bin/
sudo chmod 770 bin/*
>>>>>>> 2d454df8bfabace6cdb6e86b280f14d1ac1ba8c9

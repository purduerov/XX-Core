#!/bin/bash
sudo apt-get install -y golang 
go get github.com/graarh/golang-socketio
go get github.com/googollee/go-socket.io
go build ../pakfront/stintotcp.go 
go build ../pakfront/tcptostdin.go 
go build ../pakfront/pakfront.go ../pakfront/imgbuffer.go
mv stintotcp bin/
mv tcptostdin bin/
mv pakfront bin/
//pxytest is where we test the proxy. Should be transitioned to a dedicated pakfront.go when mature.
//It has some random functions that check things, and when enough functions related to each other are created, should be be bulbed out to a package
package main

import (
	"bufio"
	"encoding/binary"
	"fmt"
	"github.com/graarh/golang-socketio"
	"github.com/graarh/golang-socketio/transport"
	"io/ioutil"
	"log"
	"net"
	"net/http"
)

type Channel struct {
	Channel string `json:"channel"`
}

func check(e error) {
	if e != nil {
		panic("OUR ERROR FUNCTION")
	}
}

//This recives data over a tcp port and saves it in a byte array
//currently used to pick up data from the stdintotcp.go
func tcprec(port string, size int) (r int, b []byte) {
	buf := make([]byte, size)
	// listen on all interfaces
	ln, err := net.Listen("tcp", port)
	check(err)
	defer ln.Close()

	// accept connection on port
	conn, _ := ln.Accept()

	// will listen for message to process ending in newline (\n)
	read, err := bufio.NewReader(conn).Read(buf)
	check(err)

	sizein := binary.BigEndian.Uint64(buf[0:8])
	tread := read

	for tread < int(sizein)+8 {
		read, err := bufio.NewReader(conn).Read(buf[tread:])
		check(err)
		tread += read
	}
	return tread - 8, buf[8:]
}

//mjpegstreamprobe is a util function used to log what mjpegstreamer looks with no modification
//used to better copy it transparently, and find out what we can modify
func mjpegstreamprobe() {
	resp, err := http.Get("http://localhost:1917/?action=stream")
	check(err)
	data := make([]byte, 100000)
	reader := bufio.NewReader(resp.Body)
	for i := 0; i < 100000; i++ {
		d, err := reader.ReadByte()
		data[i] = d
		check(err)
	}
	tooldir := "~/foo/bar" //os.Getenv("TOOLS")
	fmt.Println(tooldir)
	err = ioutil.WriteFile(tooldir+"/bytes", data, 0644)
	check(err)
}

//main: where the magic:the gathering happens
func main() {
	server := gosocketio.NewServer(transport.GetDefaultWebsocketTransport())
	server.On(gosocketio.OnConnection, func(c *gosocketio.Channel) {
		log.Println("Conected")
	})
	server.On(gosocketio.OnDisconnection, func(c *gosocketio.Channel) {
		log.Println("Disconnected")
	})
	serveMux := http.NewServeMux()
	serveMux.Handle("/socket.io/", server)
	log.Println("Starting...")
	log.Panic(http.ListenAndServe(":5000", serveMux))
}

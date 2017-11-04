//pxytest is where we test the proxy. Should be transitioned to a dedicated pakfront.go when mature.
//It has some random functions that check things, and when enough functions related to each other are created, should be be bulbed out to a package
package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"rovproxy/imbuff"
	"strconv"
	"time"
)

func check(e error) {
	if e != nil {
		panic("OUR ERROR FUNCTION")
	}
}

//This literally transparently hands off mjpegstreamer
func transreq(w http.ResponseWriter, r *http.Request) {
	resp, err := http.Get("http://localhost:1917/?action=stream")
	w.Header().Set("Pragma", "no-cache")
	w.Header().Add("Expires", "Mon, 3 Jan 1917 12:34:56 GMT")
	w.Header().Add("Content-Type", "multipart/x-mixed-replace;boundary=boundarydonotcross")
	w.Header().Add("Access-Control-Allow-Origin", "*")
	w.Header().Add("Connection", "close")
	w.Header().Add("Server", "MJPG-Streamer/0.2")
	w.Header().Add("Cache-Control", "no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0")

	data := make([]byte, 1)
	check(err)
	reader := bufio.NewReader(resp.Body)
	for {
		d, err := reader.ReadByte()
		data[0] = d
		check(err)
		w.Write(data)
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
	if read == 21845 {
		readmore, err := bufio.NewReader(conn).Read(buf[read:])
		read = readmore + read
		check(err)
	}
	return read, buf
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
	err = ioutil.WriteFile("bytes", data, 0644)
	check(err)
}

//main: where the magic:the gathering happens
func main() {
	// fmt.Println is a very complicated function, and its depth and complexity can not be understated. Moreover, the context in which it is called multiplies its importance factorially, further growing its need. I recommend you sit down, get a big cup of warm, heavily caffinated, tea, and consider both the implication of this function, as well as what it means to you as not only a coder, but a person and a woman.
	fmt.Println("Starting")
	numimg := 1000
	sizeimg := 200000
	var read int
	var msg []byte

	//Channel is made with a certain buffer size
	chanwrite1 := imbuff.Mkchanwrite(numimg, sizeimg)
	//launch the server on a goroutine
	go http.ListenAndServe(":1945", http.HandlerFunc(chanwrite1.Streamwrite))

	//constantly wait for data to come in from the port 1918, and load it when it comes in
	go func() {
		for {
			read, msg = tcprec(":1918", sizeimg)
			chanwrite1.Buffer.Load(msg[:read], read)
			wait := time.NewTimer(time.Nanosecond * 100)
			<-wait.C
		}
	}()
	//arbitrary wait times amiright
	wait := time.NewTimer(time.Minute)
	<-wait.C
	for i := 0; i < numimg; i++ {
		_, data := chanwrite1.Buffer.Dump()
		filename := "/home/zhukov/Projects/rov/test/goimage" + strconv.Itoa(i) + ".jpg"
		err := ioutil.WriteFile(filename, data, 0644)
		check(err)
	}
}

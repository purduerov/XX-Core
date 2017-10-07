package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"time"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func transreq(w http.ResponseWriter, r *http.Request) {
	start := time.Now()
	resp, err := http.Get("http://localhost:1917/?action=stream")
	w.Header().Set("Pragma", "no-cache")
	w.Header().Add("Expires", "Mon, 3 Jan 1917 12:34:56 GMT")
	w.Header().Add("Content-Type", "multipart/x-mixed-replace;boundary=boundarydonotcross")
	w.Header().Add("Access-Control-Allow-Origin", "*")
	w.Header().Add("Connection", "close")
	w.Header().Add("Server", "MJPG-Streamer/0.2")
	w.Header().Add("Cache-Control", "no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0")
	elapsed := time.Since(start)
	fmt.Printf("Elapsed time for request: %s", elapsed)
	fmt.Print(resp.Header)
	fmt.Print("\n")

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

func tcprec(buf []byte) (read int) {
	// listen on all interfaces
	ln, _ := net.Listen("tcp", ":1918")

	// accept connection on port
	conn, _ := ln.Accept()

	// will listen for message to process ending in newline (\n)
	read, err := bufio.NewReader(conn).Read(buf)
	check(err)
	return read
}

func main() {
	msg := make([]byte, 100000)
	read := tcprec(msg)

	fmt.Printf("%x, \nRead %d Bytes\n", msg, read)

	err := ioutil.WriteFile("/tmp/im.jpg", msg, 0644)
	check(err)
}

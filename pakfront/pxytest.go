package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"time"
	"rovproxy/imbuff"
	"strconv"
)

type chanwrite struct {
	buffer imbuff.Imgbuffer
	datastm chan byte
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}


func mkchanwrite (numimg int, sizeimg int) ( writer chanwrite){
	writer.buffer = imbuff.Mkbuffer(numimg,sizeimg)
	writer.datastm = make(chan byte, 100)
	return
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

func (ch * chanwrite) streamwrite(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Pragma", "no-cache")
	w.Header().Add("Expires", "Mon, 3 Jan 1917 12:34:56 GMT")
	w.Header().Add("Content-Type", "multipart/x-mixed-replace;boundary=boundarydonotcross")
	w.Header().Add("Access-Control-Allow-Origin", "*")
	w.Header().Add("Connection", "close")
	w.Header().Add("Server", "MJPG-Streamer/0.2")
	w.Header().Add("Cache-Control", "no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0")

	for {
		read, data := ch.buffer.Dump()
		fmt.Println(ch.buffer)
		fmt.Println()

		if read > 0 {
			size :=[]byte(strconv.Itoa(read))
			w.WriteHeader(http.StatusOK)
			w.Write(imbuff.Headp1)
			w.Write(size)
			w.Write(imbuff.Headp2)
			w.Write(data)
		}
		wait := time.NewTimer(time.Nanosecond * 1000)
		<-wait.C
	}
}

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


func main() {
	numimg := 500
	sizeimg := 120000
	var read int
	var msg []byte

	chanwrite1 := mkchanwrite(numimg,sizeimg)
	go http.ListenAndServe(":8080",http.HandlerFunc(chanwrite1.streamwrite))

	go func(){
		for {
			read, msg = tcprec(":1918", sizeimg)
			chanwrite1.buffer.Load(msg[:read], read)
			fmt.Println(chanwrite1.buffer)
			fmt.Println()
		}
	}()
	wait := time.NewTimer(time.Minute * 1 )
	<-wait.C
	for i := 0; i < 3; i++ {
			read, data := chanwrite1.buffer.Dump()
			fmt.Println(read)
			if read > 0 {
				err := ioutil.WriteFile("/tmp/im.jpg", data, 0644)
				check(err)
			}
			fmt.Println(chanwrite1.buffer)
			fmt.Println()
			return
	}
	wait = time.NewTimer(time.Minute * 60 )
	<-wait.C
}

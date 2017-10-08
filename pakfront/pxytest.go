package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"time"
)

type imgbuffer struct {
	sizes []int
	data []byte
	dRptr, dWptr, datasize int
	sRptr, sWptr, numsize int
}

func (buff imgbuffer) String() string {
	return fmt.Sprintf("R Point: %v, W Point: %v\nDR Point: %v, DW Point: %v\nSizes: %v",buff.sRptr, buff.sWptr, buff.dRptr,buff.dWptr,buff.sizes)
}
func check(e error) {
	if e != nil {
		panic(e)
	}
}

func (buff * imgbuffer) load (data []byte, num int) int {

	if buff.sWptr == buff.sRptr {
		buff.dRptr = (buff.dRptr + buff.sizes[buff.sRptr])%buff.datasize
		buff.sRptr = (buff.sWptr + 1)%buff.numsize
	}

	for i := 0; i < num; i++ {
		buff.data[(i+buff.dWptr)%buff.datasize] = data[i]
	}

	buff.sizes[buff.sWptr] = num
	buff.dWptr = (buff.dWptr + num)%buff.datasize
	buff.sWptr = (buff.sWptr + 1)%buff.numsize

	return num
}

func (buff * imgbuffer) dump () (read int, img []byte ){
	size := buff.sizes[buff.sRptr]
	if size == 0 {
		return 0, nil
	}

	if (buff.sRptr + 1)%buff.numsize == buff.sWptr{
		return 0, nil
	}

	msg := make([]byte,size)
	cp := copy(msg,buff.data[buff.dRptr:buff.dRptr+buff.sizes[buff.sRptr]])

	if cp != size{
		panic("ERROR: COPY SIZE AND SIZE DONT MATCH")
	}

	buff.sRptr += 1
	buff.dRptr = (buff.dRptr+size)%buff.datasize

	return size, msg
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

func tcprec(port string,size int) (r int,b []byte) {
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
	return read, buf
}

func mjpegstreamprobe(){
	resp, err := http.Get("http://localhost:1917/?action=stream")
	check(err)
	data := make([]byte, 100000)
	reader := bufio.NewReader(resp.Body)
	for i := 0; i<100000;i++ {
		d, err := reader.ReadByte()
		data[i] = d
		check(err)
	}
	err = ioutil.WriteFile("bytes", data, 0644)
	check(err)
}
func main() {
	numimg := 5
	sizeimg := 150000
	var read int
	var msg []byte

	buf1 := imgbuffer{make([]int,numimg),make([]byte,numimg*sizeimg),0,0,numimg*sizeimg,0,1,numimg}
	for {
		read, msg = tcprec(":1918",sizeimg)
		buf1.load(msg[:read],read)
		fmt.Println(buf1)
	}

//	err := ioutil.WriteFile("/tmp/im.jpg", buf1.data[:read], 0644)
//	check(err)
}

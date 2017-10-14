package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"sync"
	"time"
)

type imgbuffer struct {
	sizes                  []int
	data                   []byte
	dRptr, dWptr, datasize int
	sRptr, sWptr, numsize  int
	mtx                    sync.Mutex
}

func (buff imgbuffer) String() string {
	return fmt.Sprintf("R Point: %v, W Point: %v\nDR Point: %v, DW Point: %v\nSizes: %v", buff.sRptr, buff.sWptr, buff.dRptr, buff.dWptr, buff.sizes)
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func (buff *imgbuffer) load(data []byte, num int) int {
	buff.mtx.Lock()
	defer buff.mtx.Unlock()

	if (buff.sWptr+1)%buff.numsize == buff.sRptr {
		buff.dRptr = (buff.dRptr + buff.sizes[buff.sRptr]) % buff.datasize
		buff.sRptr = (buff.sRptr + 1) % buff.numsize
	}

	for i := 0; i < num; i++ {
		buff.data[(i+buff.dWptr)%buff.datasize] = data[i]
	}

	buff.sizes[buff.sWptr] = num
	buff.dWptr = (buff.dWptr + num) % buff.datasize
	buff.sWptr = (buff.sWptr + 1) % buff.numsize

	return num
}

func (buff *imgbuffer) dump() (read int, img []byte) {
	buff.mtx.Lock()
	defer buff.mtx.Unlock()
	size := buff.sizes[buff.sRptr]
	if size == 0 {
		return 0, nil
	}

	if buff.sRptr == buff.sWptr {
		return 0, nil
	}

	msg := make([]byte, size)
	cp := copy(msg, buff.data[buff.dRptr:buff.dRptr+buff.sizes[buff.sRptr]])

	if cp != size {
		panic("ERROR: COPY SIZE AND SIZE DONT MATCH")
	}

	buff.sRptr = (buff.sRptr + 1) % buff.numsize
	buff.dRptr = (buff.dRptr + size) % buff.datasize

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

func mkbuffer(nImg int, nSize int) (buf imgbuffer ){
	buf.sizes = make([]int, nImg)
	buf.data = make([]byte, nImg*nSize)
	buf.dRptr = 0
	buf.dWptr = 0
	buf.datasize = nImg * nSize
	buf.sRptr = 0
	buf.sWptr = 0
	buf.numsize = nImg
	return
}

func main() {
	numimg := 6
	sizeimg := 100000
	var read int
	var msg []byte

	buf1 := mkbuffer(numimg,sizeimg)

	for i := 0; i < 5; i++ {
			read, msg = tcprec(":1918", sizeimg)
			buf1.load(msg[:read], read)
			fmt.Println(buf1)
			fmt.Println()
	}

	for i := 0; i < 3; i++ {
		go func(){
			read, data := buf1.dump()
			fmt.Println(read)
			if read > 0 {
				err := ioutil.WriteFile("/tmp/im.jpg", data, 0644)
				check(err)
			}
			fmt.Println(buf1)
			fmt.Println()
			return
		}()
	}

}

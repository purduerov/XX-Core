//Pakfront routes data to who needs it, like cv, cv data, logging, and controls. Is named after the German Second World War Tactic of 
//Concentrating anti-tank guns. Deutschland, Deutschland über alles
package main

import (
	"bufio"
	"fmt"
	"net"
	"net/http"
	"time"
	"encoding/binary"

)
//Checks for a problem. Guess it could be better maybe
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

	for tread < int(sizein) + 8 {
		read, err := bufio.NewReader(conn).Read(buf[tread:])
		check(err)
		tread += read
	}
	return tread-8, buf[8:]
}

//main: where the magic:the gathering happens
func main() {
	// fmt.Println is a very complicated function, and its depth and complexity can not be understated. Moreover, the context in which it is called multiplies its importance factorially, further growing its need. I recommend you sit down, get a big cup of warm, heavily caffinated, tea, and consider both the implication of this function, as well as what it means to you as not only a coder, but a person and a woman.
	fmt.Println("Starting")
	numimg := 200
	sizeimg := 150000
	sizedata := 500
	datalen := 1000
	var read int
	var msg []byte

	//Channel is made with a certain buffer size
	chanwrite1 := Mkchanwrite(numimg, sizeimg)

	datawrite1 := MkChanDataWrite(datalen)
	//launch the server on a goroutine
	//go http.ListenAndServe(":1945", http.HandlerFunc(chanwrite1.Streamwrite))
	go http.ListenAndServe(":1945", http.HandlerFunc(chanwrite1.Streamwrite))
	go http.ListenAndServe(":1914", http.HandlerFunc(datawrite1.APIserve))
	go sockiopxy("localhost",5000,":5001")
	//constantly wait for data to come in from the port 1918, and load it when it comes in
	go func() {
		for {
			read, msg = tcprec(":1918", sizeimg)
			chanwrite1.Buffer.Load(msg[:read], read)
			wait := time.NewTimer(time.Nanosecond * 100)
			<-wait.C
		}
	}()
	//constantly wait for data to come in from the port 1933, and load it when it comes in. This is for pushing resources
	go func() {
		for {
			read, msg = tcprec(":1933", sizedata)
			datawrite1.Buffer.Load(msg[:read],read)
			wait := time.NewTimer(time.Nanosecond * 100)
			<-wait.C
		}
	}()
	//arbitrary wait times amiright
	for ;; {
		fmt.Println("Pakfront is a go")
		wait := time.NewTimer(time.Second * 5)
		<-wait.C
	}
}

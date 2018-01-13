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
	"io/ioutil"
	"encoding/json"
	"strconv"

)

type Socketio struct{
	Port_to_rov int
	Port_to_client int
}

type Process struct{
	Name string
	ID int
}

type Cvhandler struct{
	Number_of_images int
	Size_of_image int
	Size_of_data int
	Num_processes int
	Processes []Process
}

type config struct {
	Socketio Socketio
	Cvhandler Cvhandler
}

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

func getconfig(filename string) config{
	content, err := ioutil.ReadFile(filename)
	check(err)
	var ret config
	err = json.Unmarshal(content, &ret)
	check(err)
	return ret

}
func numtoportstr(port int) string {
	return ":" + strconv.Itoa(port)
}
func cvproc(conf config, procnum int) {
	var read int
	var msg []byte
	numimg := conf.Cvhandler.Number_of_images
	sizeimg := conf.Cvhandler.Size_of_image
	sizedata := conf.Cvhandler.Size_of_data


	to_client_video :=4*conf.Cvhandler.Processes[procnum].ID + 1 + 1917
	to_client_data :=4*conf.Cvhandler.Processes[procnum].ID + 2 + 1917
	to_cv_process :=4*conf.Cvhandler.Processes[procnum].ID + 3 + 1917
	to_cv_process_data :=4*conf.Cvhandler.Processes[procnum].ID + 4 + 1917
	fmt.Printf("{\"name\": \"%v\", \"stream\": %v, \"data\": %v}\n",
			conf.Cvhandler.Processes[procnum].Name,
			to_client_video,
			to_client_data)

	//Channel is made with a certain buffer size
	chanwrite1 := Mkchanwrite(numimg, sizeimg)

	datawrite1 := MkChanDataWrite(sizedata)
	//launch the server on a goroutine
	go http.ListenAndServe(numtoportstr(to_client_video), http.HandlerFunc(chanwrite1.Streamwrite))
	go http.ListenAndServe(numtoportstr(to_client_data), http.HandlerFunc(datawrite1.APIserve))
	//constantly wait for data to come in from the port 1918, and load it when it comes in
	go func() {
		for {
			read, msg = tcprec(numtoportstr(to_cv_process), sizeimg)
			chanwrite1.Buffer.Load(msg[:read], read)
			wait := time.NewTimer(time.Nanosecond * 100)
			<-wait.C
		}
	}()
	//constantly wait for data to come in from the port 1933, and load it when it comes in. This is for pushing resources
	go func() {
		for {
			read, msg = tcprec(numtoportstr(to_cv_process_data), sizedata)
			datawrite1.Buffer.Load(msg[:read],read)
			wait := time.NewTimer(time.Nanosecond * 100)
			<-wait.C
		}
	}()

}

//main: where the magic:the gathering happens
func main() {

	// fmt.Println is a very complicated function, and its depth and complexity can not be understated. Moreover, the context in which it is called multiplies its importance factorially, further growing its need. I recommend you sit down, get a big cup of warm, heavily caffinated, tea, and consider both the implication of this function, as well as what it means to you as not only a coder, but a person and a woman.
	conf := getconfig("proxyconfig.json")

	numProc := conf.Cvhandler.Num_processes
	fmt.Println(conf.Socketio.Port_to_rov)
	go sockiopxy("10.42.0.234", conf.Socketio.Port_to_rov, numtoportstr(conf.Socketio.Port_to_client))

	procnum := 0
	for procnum < numProc {
		go cvproc(conf, procnum)
		procnum++
	}

	//arbitrary wait times amiright
	for ;; {
		wait := time.NewTimer(time.Second * 5)
		<-wait.C
		fmt.Println("Pakfront is a go")
	}
}

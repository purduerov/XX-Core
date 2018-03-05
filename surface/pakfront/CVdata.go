//can you SEE the letter VEEE idk if that was a joke or something but I guess this is the place where the CV found data is handed
package main

import (
	"fmt"
	"net/http"
	"sync"
	"time"
)

//The CV data buffer
type CVdata struct {
	Data []byte
	size int
	mtx  sync.Mutex
}

//The streamer
type datawrite struct {
	Buffer  CVdata
	datastm chan byte
}

//To print the data
func (buff CVdata) String() string {
	return fmt.Sprintf("Data: %v\nSize: %v\n", string(buff.Data), buff.size)
}

//Loads the data into the CV buffer
func (buff *CVdata) Load(Data []byte, num int) int {
	buff.mtx.Lock()
	defer buff.mtx.Unlock()
	buff.size = num

	for i := 0; i < num; i++ {
		buff.Data[i] = Data[i]
	}
	return num
}

//Outputs the data from the cv buffer
func (buff *CVdata) Dump() (read int, img []byte) {
	buff.mtx.Lock()
	defer buff.mtx.Unlock()
	msg := make([]byte, buff.size)
	if buff.size == 0 {
		return 0, nil
	}
	copy(msg, buff.Data[:buff.size])

	return buff.size, msg

}

//Makes the buffer
func MkDataBuff(datalen int) (buf CVdata) {
	buf.Data = make([]byte, datalen)
	buf.size = 0
	return buf
}

//Makes the stream
func MkChanDataWrite(datalen int) (writer datawrite) {
	writer.Buffer = MkDataBuff(datalen)
	writer.datastm = make(chan byte, datalen)
	return
}

//Function to serve the data
func (ch *datawrite) APIserve(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Stalin", "You know stalin is one of those guys who really was a pretty bad guy")
	w.Header().Set("Date", "Sat, 1 Jan 2000 12:00:00 GMT")
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_, data := ch.Buffer.Dump()
	_, err := w.Write(data)
	check(err)
	//Give time for the mutex to unlactch. not the most elegant thing
	wait := time.NewTimer(time.Nanosecond * 1000)
	<-wait.C
}

package main

import(
	"sync"
	"fmt"
	"net/http"
	"time"
)
type CVdata struct {
	Data                   []byte
	size				   int
	mtx                    sync.Mutex
}

type datawrite struct {
	Buffer  CVdata
	datastm chan byte
}

func (buff CVdata) String() string {
	return fmt.Sprintf("Data: %v\nSize: %v\n",string(buff.Data),buff.size)
}

func (buff *CVdata) Load(Data []byte, num int) int {
	buff.mtx.Lock()
	defer buff.mtx.Unlock()
	buff.size = num

	for i := 0; i < num; i++ {
		buff.Data[i] = Data[i]
	}
	return num
}

func (buff *CVdata) Dump() (read int, img []byte) {
	buff.mtx.Lock()
	defer buff.mtx.Unlock()
	msg := make([]byte,buff.size)
	if buff.size == 0 {
		return 0, nil
	}
	fmt.Println(buff.Data)
	copy(msg,buff.Data[:buff.size])
	fmt.Println(msg)

	return buff.size, msg

}

func MkDataBuff(datalen int) (buf CVdata){
	buf.Data = make([]byte,datalen)
	buf.size = 0
	return buf
}

func MkChanDataWrite(datalen int)(writer datawrite){
	writer.Buffer = MkDataBuff(datalen)
	writer.datastm = make(chan byte, datalen )
	return
}

func (ch *datawrite) APIserve(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	_, data := ch.Buffer.Dump()
	fmt.Println(data)
	_, err := w.Write(data)
	check(err)
	wait := time.NewTimer(time.Nanosecond * 1000)
	<-wait.C
}

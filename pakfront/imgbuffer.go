//imbuff implements a circular buffer that stores images, to serve as a static stream
//It's not complicated, seriously just read it.
package imbuff

import (
	"fmt"
	"sync"
)

type Imgbuffer struct {
	Sizes                  []int
	Data                   []byte
	DRptr, DWptr, Datasize int
	SRptr, SWptr, numsize  int
	mtx                    sync.Mutex
}

//Headers are for delimiting the image boundries for the browser. Copied directly from a stream without this proxy
var Headp1 = []byte{0x2d, 0x2d, 0x62, 0x6f, 0x75, 0x6e, 0x64, 0x61, 0x72, 0x79, 0x64, 0x6f, 0x6e, 0x6f, 0x74, 0x63, 0x72, 0x6f, 0x73, 0x73, 0xd, 0xa, 0x43, 0x6f, 0x6e, 0x74, 0x65, 0x6e, 0x74, 0x2d, 0x54, 0x79, 0x70, 0x65, 0x3a, 0x20, 0x69, 0x6d, 0x61, 0x67, 0x65, 0x2f, 0x6a, 0x70, 0x65, 0x67, 0xd, 0xa, 0x43, 0x6f, 0x6e, 0x74, 0x65, 0x6e, 0x74, 0x2d, 0x4c, 0x65, 0x6e, 0x67, 0x74, 0x68, 0x3a, 0x20}
var Headp2 = []byte{0x0d, 0x0a, 0x58, 0x2d, 0x54, 0x69, 0x6d, 0x65, 0x73, 0x74, 0x61, 0x6d, 0x70, 0x3a, 0x20, 0x31, 0x38, 0x37, 0x37, 0x2e, 0x39, 0x36, 0x37, 0x30, 0x33, 0x32, 0x0d, 0x0a, 0x0d, 0x0a}

//String implements the String interface for Imgbuffer.
//Prints out all relevant information
func (buff Imgbuffer) String() string {
	return fmt.Sprintf("R Point: %v, W Point: %v\nDR Point: %v, DW Point: %v\nSizes: %v", buff.SRptr, buff.SWptr, buff.DRptr, buff.DWptr, buff.Sizes)
}

//Load takes Data, and the amount of bytes and saves it into the buffer
//Currently Load and Dump are mutually exclusive with a mutex
func (buff *Imgbuffer) Load(Data []byte, num int) int {
	buff.mtx.Lock()
	defer buff.mtx.Unlock()

	if (buff.SWptr+1)%buff.numsize == buff.SRptr {
		buff.DRptr = (buff.DRptr + buff.Sizes[buff.SRptr]) % buff.Datasize
		buff.SRptr = (buff.SRptr + 1) % buff.numsize
	}

	for i := 0; i < num; i++ {
		buff.Data[(i+buff.DWptr)%buff.Datasize] = Data[i]
	}

	//Moves the pointers properly
	buff.Sizes[buff.SWptr] = num
	buff.DWptr = (buff.DWptr + num) % buff.Datasize
	buff.SWptr = (buff.SWptr + 1) % buff.numsize

	return num
}

//Dump outputs a bytearray of data from the buffer
//Currently Load and Dump are mutually exclusive with a mutex
func (buff *Imgbuffer) Dump() (read int, img []byte) {
	buff.mtx.Lock()
	defer buff.mtx.Unlock()
	size := buff.Sizes[buff.SRptr]
	//If the data is empty, or if the buffer is empty, return 0
	if size == 0 {
		return 0, nil
	}

	if buff.SRptr == buff.SWptr {
		return 0, nil
	}

	msg := make([]byte, size)
	cp := copy(msg, buff.Data[buff.DRptr:buff.DRptr+buff.Sizes[buff.SRptr]])

	if cp != size {
		panic("ERROR: COPY SIZE AND SIZE DONT MATCH")
	}

	//Moves the pointers properly
	buff.SRptr = (buff.SRptr + 1) % buff.numsize
	buff.DRptr = (buff.DRptr + size) % buff.Datasize

	return size, msg
}

//Mkbuffer creates an imbuffer that can hold nImg images of max size nSize
func Mkbuffer(nImg int, nSize int) (buf Imgbuffer) {
	buf.Sizes = make([]int, nImg)
	buf.Data = make([]byte, nImg*nSize)
	buf.DRptr = 0
	buf.DWptr = 0
	buf.Datasize = nImg * nSize
	buf.SRptr = 0
	buf.SWptr = 0
	buf.numsize = nImg
	return
}

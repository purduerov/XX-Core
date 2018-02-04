//imbuff implements a circular buffer that stores images, to serve as a static stream
//It's not complicated, seriously just read it.
package main

import (
	"fmt"
	"net/http"
	"strconv"
	"sync"
	"time"
)

type Imgbuffer struct {
	Sizes                  []int
	Data                   []byte
	DRptr, DWptr, Datasize int
	SRptr, SWptr, numsize  int
	mtx                    sync.Mutex
}

type chanwrite struct {
	Buffer  Imgbuffer
	datastm chan byte
}

//Headers are for delimiting the image boundries for the browser. Copied directly from a stream without this proxy
var Headp1 = []byte{0x2d, 0x2d, 0x62, 0x6f, 0x75, 0x6e, 0x64, 0x61, 0x72, 0x79, 0x64, 0x6f, 0x6e, 0x6f, 0x74, 0x63, 0x72, 0x6f, 0x73, 0x73, 0xd, 0xa, 0x43, 0x6f, 0x6e, 0x74, 0x65, 0x6e, 0x74, 0x2d, 0x54, 0x79, 0x70, 0x65, 0x3a, 0x20, 0x69, 0x6d, 0x61, 0x67, 0x65, 0x2f, 0x6a, 0x70, 0x65, 0x67, 0xd, 0xa, 0x43, 0x6f, 0x6e, 0x74, 0x65, 0x6e, 0x74, 0x2d, 0x4c, 0x65, 0x6e, 0x67, 0x74, 0x68, 0x3a, 0x20}
var Headp2 = []byte{0x0d, 0x0a, 0x58, 0x2d, 0x54, 0x69, 0x6d, 0x65, 0x73, 0x74, 0x61, 0x6d, 0x70, 0x3a, 0x20, 0x31, 0x38, 0x37, 0x37, 0x2e, 0x39, 0x36, 0x37, 0x30, 0x33, 0x32, 0x0d, 0x0a, 0x0d, 0x0a}

//String implements the String interface for Imgbuffer.
//Prints out all relevant information
func (buff Imgbuffer) String() string {
	return fmt.Sprintf("R Point: %v, W Point: %v\nDR Point: %v, DW Point: %v\nIm Size: %v\n\n", buff.SRptr, buff.SWptr, buff.DRptr, buff.DWptr, buff.Sizes[buff.SRptr])
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
	var msg []byte
	size := buff.Sizes[buff.SRptr]
	//If the data is empty, or if the buffer is empty, return 0
	if size == 0 {
		return 0, nil
	}

	if buff.SRptr == buff.SWptr {
		return 0, nil
	}

	if buff.DRptr+buff.Sizes[buff.SRptr] < buff.Datasize {
		msg = buff.Data[buff.DRptr : buff.DRptr+buff.Sizes[buff.SRptr]]
	} else {
		startChunk := buff.DRptr + buff.Sizes[buff.SRptr]
		msg = append(buff.Data[buff.DRptr:buff.Datasize], buff.Data[0:startChunk%buff.Datasize]...)
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

/*
                   ,-'     `._
                 ,'           `.        ,-.
               ,'               \       ),.\
     ,.       /                  \     /(  \;
    /'\\     ,o.        ,ooooo.   \  ,'  `-')
    )) )`. d8P"Y8.    ,8P"""""Y8.  `'  .--"'
   (`-'   `Y'  `Y8    dP       `'     /
    `----.(   __ `    ,' ,---.       (
           ),--.`.   (  ;,---.        )
          / \O_,' )   \  \O_,'        |
         ;  `-- ,'       `---'        |
         |    -'         `.           |
        _;    ,            )          :
     _.'|     `.:._   ,.::" `..       |
  --'   |   .'     """         `      |`.
        |  :;      :   :     _.       |`.`.-'--.
        |  ' .     :   :__.,'|/       |  \
        `     \--.__.-'|_|_|-/        /   )
         \     \_   `--^"__,'        ,    |
   -hrr- ;  `    `--^---'          ,'     |
          \  `                    /      /
           \   `    _ _          /
            \           `       /
             \           '    ,'
              `.       ,   _,'
                `-.___.---'
*/
func Mkchanwrite(numimg int, sizeimg int) (writer chanwrite) {
	writer.Buffer = Mkbuffer(numimg, sizeimg)
	writer.datastm = make(chan byte, 100)
	return
}

func (ch *chanwrite) Imwrite(w http.ResponseWriter, r *http.Request) {

	w.Header().Set("Pragma", "no-cache")
	w.Header().Add("Access-Control-Allow-Origin", "*")
	w.Header().Add("Connection", "close")
	w.Header().Add("Server", "MJPG-Streamer/0.2")
	w.Header().Add("Cache-Control", "no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0")
	w.WriteHeader(http.StatusOK)
	_, data := ch.Buffer.Dump()
	_, err := w.Write(data)
	check(err)
	return
}

// This sets up the chanwrite as a server that streams its buffer
func (ch *chanwrite) Streamwrite(w http.ResponseWriter, r *http.Request) {
	// Necessary headers (found by viewing no proxy headers)
	w.Header().Set("Pragma", "no-cache")
	w.Header().Add("Expires", "Mon, 3 Jan 1917 12:34:56 GMT")
	w.Header().Add("Content-Type", "multipart/x-mixed-replace;boundary=boundarydonotcross")
	w.Header().Add("Access-Control-Allow-Origin", "*")
	w.Header().Add("Connection", "close")
	w.Header().Add("Server", "MJPG-Streamer/0.2")
	w.Header().Add("Cache-Control", "no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0")
	w.WriteHeader(http.StatusOK)

	var twritten int // Total written of this frame
	var written int  // Written of this chunk
	//Stream
	for {
		//Get this frame in data
		read, data := ch.Buffer.Dump()
		twritten = 0
		written = 0
		if read > 0 {
			//Write out the header delimiter
			size := []byte(strconv.Itoa(read))
			w.Write(Headp1)
			w.Write(size)
			w.Write(Headp2)
			//While we have not written the whole frame, write
			for twritten < read {
				written, err := w.Write(data[written:])
				check(err)
				twritten += written
			}
		}
		//slight delay for the mutex write to buffer to occur. Possibly come up with a more elegant solution
		wait := time.NewTimer(time.Nanosecond * 1000)
		<-wait.C
	}
}

package imbuff
import(
	"sync"
	"fmt"
)

type Imgbuffer struct {
	sizes                  []int
	data                   []byte
	dRptr, dWptr, datasize int
	sRptr, sWptr, numsize  int
	mtx                    sync.Mutex
}

func (buff Imgbuffer) String() string {
	return fmt.Sprintf("R Point: %v, W Point: %v\nDR Point: %v, DW Point: %v\nSizes: %v", buff.sRptr, buff.sWptr, buff.dRptr, buff.dWptr, buff.sizes)
}


func (buff *Imgbuffer) Load(data []byte, num int) int {
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

func (buff *Imgbuffer) Dump() (read int, img []byte) {
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

func Mkbuffer(nImg int, nSize int) (buf Imgbuffer ){
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


package imbuff
import(
	"sync"
	"fmt"
)

type Imgbuffer struct {
	Sizes                  []int
	Data                   []byte
	DRptr, DWptr, Datasize int
	SRptr, SWptr, numsize  int
	mtx                    sync.Mutex
}

var Headp1 = []byte{0x2d, 0x2d, 0x62, 0x6f, 0x75, 0x6e, 0x64, 0x61, 0x72, 0x79, 0x64, 0x6f, 0x6e, 0x6f, 0x74, 0x63, 0x72, 0x6f, 0x73, 0x73, 0xd, 0xa, 0x43, 0x6f, 0x6e, 0x74, 0x65, 0x6e, 0x74, 0x2d, 0x54, 0x79, 0x70, 0x65, 0x3a, 0x20, 0x69, 0x6d, 0x61, 0x67, 0x65, 0x2f, 0x6a, 0x70, 0x65, 0x67, 0xd, 0xa, 0x43, 0x6f, 0x6e, 0x74, 0x65, 0x6e, 0x74, 0x2d, 0x4c, 0x65, 0x6e, 0x67, 0x74, 0x68, 0x3a, 0x20}
var Headp2 = []byte{0x0d, 0x0a, 0x58, 0x2d, 0x54, 0x69, 0x6d, 0x65, 0x73, 0x74, 0x61, 0x6d, 0x70, 0x3a, 0x20, 0x31, 0x38, 0x37, 0x37, 0x2e, 0x39, 0x36, 0x37, 0x30, 0x33, 0x32, 0x0d, 0x0a, 0x0d, 0x0a}


func (buff Imgbuffer) String() string {
	return fmt.Sprintf("R Point: %v, W Point: %v\nDR Point: %v, DW Point: %v\nSizes: %v", buff.SRptr, buff.SWptr, buff.DRptr, buff.DWptr, buff.Sizes)
}


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

	buff.Sizes[buff.SWptr] = num
	buff.DWptr = (buff.DWptr + num) % buff.Datasize
	buff.SWptr = (buff.SWptr + 1) % buff.numsize

	return num
}

func (buff *Imgbuffer) Dump() (read int, img []byte) {
	buff.mtx.Lock()
	defer buff.mtx.Unlock()
	size := buff.Sizes[buff.SRptr]
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

	buff.SRptr = (buff.SRptr + 1) % buff.numsize
	buff.DRptr = (buff.DRptr + size) % buff.Datasize

	return size, msg
}

func Mkbuffer(nImg int, nSize int) (buf Imgbuffer ){
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


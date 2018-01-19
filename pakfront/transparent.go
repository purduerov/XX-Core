package main

import (
	"bufio"
	"fmt"
	"net/http"
)

type Trans struct {
	ip         string
	reqport    int
	camnum     int
	serverport int
	status     int
}

//This literally transparently hands off mjpegstreamer
func (serv *Trans) Transreq(w http.ResponseWriter, r *http.Request) {
	if serv.status == 404 {
		w.WriteHeader(404)
		return
	}
	resp, err := http.Get(fmt.Sprintf("http://%v:%v/?action=stream_%v", serv.ip, serv.reqport, serv.camnum))
	w.Header().Set("Pragma", "no-cache")
	w.Header().Add("Expires", "Mon, 3 Jan 1917 12:34:56 GMT")
	w.Header().Add("Content-Type", "multipart/x-mixed-replace;boundary=boundarydonotcross")
	w.Header().Add("Access-Control-Allow-Origin", "*")
	w.Header().Add("Connection", "close")
	w.Header().Add("Server", "MJPG-Streamer/0.2")
	w.Header().Add("Cache-Control", "no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0")

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

func Mktrans(ip string, reqport int, camnum int, serverport int) (ret Trans) {
	resp, err := http.Get(fmt.Sprintf("http://%v:%v/?action=snapshot_%v", ip, reqport, camnum))
	check(err)
	ret.status = resp.StatusCode
	ret.ip = ip
	ret.reqport = reqport
	ret.camnum = camnum
	ret.serverport = serverport
	return ret

}

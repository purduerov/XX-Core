package main

import (
	"log"
	"net/http"
	"runtime"

	"github.com/graarh/golang-socketio"
	"github.com/graarh/golang-socketio/transport"
	"github.com/googollee/go-socket.io"
)

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU())

	pxyToROV, err := gosocketio.Dial(
		gosocketio.GetUrl("localhost", 5000, false),
		transport.GetDefaultWebsocketTransport())
	if err != nil {
		log.Fatal(err)
	}

	pxyToClient, err := socketio.NewServer(nil)
	if err != nil {
		log.Fatal(err)
	}

	pxyToClient.On("connection", func(so socketio.Socket) {
		pxyToROV.On("dearflask", func(c *gosocketio.Channel, msg string) string {
			so.Emit("dearflask")
			return "Done"
		})
		pxyToROV.On("dearclient", func(c *gosocketio.Channel, msg string) string {
			so.Emit("dearclient",msg)
			return "Done"
		})

		so.On("dearclient", func(msg string) {
			pxyToROV.Emit("dearclient","")
		})

		so.On("dearflask", func(msg string) {
			pxyToROV.Emit("dearflask", msg)
		})


		so.On("disconnection", func() {
		})
	})

	pxyToClient.On("error", func(so socketio.Socket, err error) {
		log.Println("error:", err)
	})

	http.Handle("/socket.io/", pxyToClient)
	http.Handle("/", http.FileServer(http.Dir("./asset")))
	log.Println("Serving at localhost:5001...")
	log.Fatal(http.ListenAndServe(":5001", nil))
	return
}

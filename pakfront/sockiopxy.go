package main

import (
	"log"
	"net/http"
	"runtime"

	"github.com/graarh/golang-socketio"
	"github.com/graarh/golang-socketio/transport"
	"github.com/googollee/go-socket.io"
)

func sockiopxy(rovIP string, rovPort int, clientPort string){
		runtime.GOMAXPROCS(runtime.NumCPU())

	pxyToROV, err := gosocketio.Dial(
		gosocketio.GetUrl(rovIP, rovPort, false),
		transport.GetDefaultWebsocketTransport())
	check(err)

	pxyToClient, err := socketio.NewServer(nil)
	check(err)

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
	log.Fatal(http.ListenAndServe(clientPort, nil))
	return
}
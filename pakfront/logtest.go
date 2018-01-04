package main

import (
	"log"
	"net/http"
	"runtime"

	"github.com/graarh/golang-socketio"
	"github.com/graarh/golang-socketio/transport"
	"github.com/googollee/go-socket.io"
)

type Channel struct {
	Channel float64 `json:"last_update"`
}

type Message struct {
	Id      int    `json:"id"`
	Channel string `json:"channel"`
	Text    string `json:"text"`
}

func main() {
	type Packet struct {
		Data string
	}

	//datadown := Packet{"{\"down\":1}"}
	//dataup := Packet{"{\"up\":2}"}
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
		log.Println("Proxy to Client Connect")
		pxyToROV.On("dearflask", func(c *gosocketio.Channel, msg Channel) string {
			log.Println("Got DearFlask from Rov")
			so.Emit("dearflask")
			return "Done"
		})
		pxyToROV.On("dearclient", func(c *gosocketio.Channel, msg Channel) string {
			log.Println("Got Dearclient from Rov")
			log.Println("Data")
			log.Println(msg)
			so.Emit("dearclient",msg)
			return "Done"
		})

		so.On("dearclient", func(msg string) {
			log.Println("Got DearClient from Client")
			pxyToROV.Emit("dearclient","")
		})

		so.On("dearflask", func(msg string) {
			log.Println("Got DearFlask from Client")
			pxyToROV.Emit("dearflask", msg)
		})


		so.On("disconnection", func() {
			log.Println("Proxy To Client Disconnect")
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

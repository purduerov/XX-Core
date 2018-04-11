//Transparently handles and logs the socketio transactions. Also allows us to easiy send commands down to the ROV
package main

import (
	"log"
	"net/http"
	"os"
	"runtime"

	"github.com/googollee/go-socket.io"
	"github.com/graarh/golang-socketio"
	"github.com/graarh/golang-socketio/transport"
)

func sockiopxy(rovIP string, rovPort int, clientPort string) {
	//Makes it so we do not consume to many resources
	path := os.Getenv("LOGDIR")
	if len(path) == 0 {
		path = "."
	}

	fileopener := openfile(path)

	runtime.GOMAXPROCS(runtime.NumCPU())

	//Connects to the ROV
	pxyToROV, err := gosocketio.Dial(
		gosocketio.GetUrl(rovIP, rovPort, false),
		transport.GetDefaultWebsocketTransport())
	check(err)

	//Waits for a connection from the client
	pxyToClient, err := socketio.NewServer(nil)

	check(err)

	//When the client connects, the transactions begin
	pxyToClient.On("connection", func(so socketio.Socket) {
		//All it does is bounce the data through, while logging
		pxyToROV.On("dearflask", func(c *gosocketio.Channel, msg string) string {
			so.Emit("dearflask")
			return "Done"
		})
		pxyToROV.On("dearclient", func(c *gosocketio.Channel, msg interface{}) string {
			so.Emit("dearclient", msg)
			packClient(msg, fileopener)

			return "Done"
		})

		so.On("dearclient", func(msg string) {
			pxyToROV.Emit("dearclient", "")
		})

		so.On("dearflask", func(msg interface{}) {
			pxyToROV.Emit("dearflask", msg)
			packFlask(msg, fileopener)
		})

		so.On("disconnection", func() {
		})
	})

	pxyToClient.On("error", func(so socketio.Socket, err error) {
		log.Println("error:", err)
	})

	//Launch server
	http.Handle("/socket.io/", pxyToClient)
	http.Handle("/", http.FileServer(http.Dir("./bin")))
	log.Fatal(http.ListenAndServe(clientPort, nil))
	return
}

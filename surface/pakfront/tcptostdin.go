//tcptostdin reads an image from the mjpeg streamer on localhost, and writes the image to stdin
//We will need to configure it to dynamically find the ip to request from
package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

func check(e error) {
	if e != nil {
		fmt.Println(e)
		os.Exit(1)
	}

}

// Like I dont think you fully understand how trivial this. Like seriously.
func main() {
	args := os.Args[1:]
	if len(args) < 3 {
		fmt.Println(" ")
		os.Exit(1)
	}
	port := args[0]
	camnum := args[1]
	ip := args[2]
	resp, err := http.Get("http://" + ip + ":" + port + "/?action=snapshot_" + camnum)
	check(err)
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	check(err)
	fmt.Printf("%s", body)
}

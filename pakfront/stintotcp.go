//stintotcp reads bytes from stdin and outputs it on a tcp port 
//Currently configured to just output on localhost
package main

import (
	"fmt"
	"net"
	"os"
)

func check(e error) {
	if e != nil {
		fmt.Printf("connection start\n")
		conn, err := net.Dial("tcp", "192.168.1.112:53")
		fmt.Printf("Connected\n")
	}

}

//Its pretty self explanatory. Like seriously. Just understand it.
func main() {
	bytes := make([]byte, 9999)
	fmt.Printf("connection start\n")
	conn, err := net.Dial("tcp", "192.168.1.112:53")
	check(err)
	fmt.Printf("Connected\n")
	wrote := 0
	for {
		fmt.Println("writing")
		w, err := conn.Write(bytes)
		check(err)
		wrote += w
	}
}

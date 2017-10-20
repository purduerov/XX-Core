//stintotcp reads bytes from stdin and outputs it on a tcp port
//Currently configured to just output on localhost
package main

import (
	"fmt"
	"io/ioutil"
	"net"
	"os"
)

func check(e error) {
	if e != nil {
		fmt.Println(e)
		os.Exit(1)
	}

}

//Its pretty self explanatory. Like seriously. Just understand it.
func main() {
	bytes, err := ioutil.ReadAll(os.Stdin)
	conn, err := net.Dial("tcp", "127.0.0.1:1918")
	check(err)
	num, err := conn.Write(bytes[5:])
	check(err)
	fmt.Println("go has written: ", num)
}

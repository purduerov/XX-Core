package main

import (
	"fmt"
	"os"
	"net/http"
	"io/ioutil"
)

func check(e error) {
	if e != nil {
		fmt.Println(e)
		os.Exit(1)
	}

}
func main() {
	resp, err := http.Get("http://localhost:1917/?action=snapshot")
	check(err)
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	check(err)
	fmt.Printf("%s",body)
}

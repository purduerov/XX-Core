package main

import (
	"encoding/json"
	"log"
	"os"
	"time"
)

type FileOpener struct {
	dearClientFile *os.File
	dearflaskFile  *os.File
}

// func check(e error) { // error checking function
//     if e != nil {
//         panic(e)
//     }
// }

func packClient(s string, f FileOpener) { //logging the client messages in JSON format
	b, _ := json.Marshal(s)

	if _, err := f.dearClientFile.Write([]byte(b)); err != nil { // data
		log.Fatal(err)
	}
	if _, err := f.dearClientFile.Write([]byte("\r\n")); err != nil { // new line
		log.Fatal(err)
	}
}

func packFlask(s string, f FileOpener) { //logging the flask messages in JSON format
	b, _ := json.Marshal(s)

	if _, err := f.dearflaskFile.Write([]byte(b)); err != nil { // data
		log.Fatal(err)
	}
	if _, err := f.dearflaskFile.Write([]byte("\r\n")); err != nil { // new line
		log.Fatal(err)
	}
}

func openfile(pat string) FileOpener {
	t := time.Now()
	tim := t.Format("2006_01_02__15_04_05")
	//	fmt.Println(tim)

	path := pat + "/" + tim //setting the path for the folder in the format YYYY_MM_DD__HH_MM_SS
	//	fmt.Println(path)

	if _, err := os.Stat(path); os.IsNotExist(err) {
		os.Mkdir(path, os.FileMode(os.ModePerm)) //Creating the folder
	}

	clientlogfile := path + "/dearclientlog.txt" //path to the client file in the folder
	flasklogfile := path + "/dearflaskFile.txt"  //path to the flask file in the folder

	log.Println(clientlogfile)

	f, err := os.Create(clientlogfile) // create file if doesn't exist

	check(err)

	f1, err := os.Create(flasklogfile) // create file if doesn't exist

	check(err)

	fileopener := FileOpener{dearClientFile: f, dearflaskFile: f1}
	return fileopener
}

// func main() {

// 	//path := "C:\\Users\\Mudabbir\\Documents\\XX-Core\\rov\\sensors\\powerboard\\Package\\" + tim

// 	s := "{\"thrusters\": {\"desired_thrust\": [2, 2, 2, 2, 2, 2],\"disabled_thrusters\": [],\"thruster_scales\n\": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]},\"valve_turner\": {\"power\": 0.0},\"claw\": {\"power\": 0.0},\"fountain_tool\": {\"power\": 0.0},\"cameras\": [ { \"port\": 8080, \"status\": 1 },{ \"port\": 8081, \"status\": 0 },{ \"port\": 8082, \"status\": 1 },{ \"port\": 8083, \"status\": 0 },{ \"port\": 8084, \"status\": 1 },{ \"port\": 8085, \"status\": 1 },]}"
// 	//fmt.Println(s)

// 	path := os.Getenv("FOO")

// 	fileopener := openfile(path)
// 	packClient(s,fileopener);
// 	packFlask(s,fileopener);
// 	packClient(s,fileopener);
// 	packClient(s,fileopener);
// 	packClient(s,fileopener);

// }

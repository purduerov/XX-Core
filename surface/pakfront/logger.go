package main

import (
	"encoding/json" // to encode in JSON format
	"log"           // to print out an error if we have any
	"os"            // to perform OS functions
	"time"          // to create the file with respect to current time
)

type FileOpener struct {
	clientFile *os.File // the names of the two files I wanted to log
	flaskFile  *os.File
}

func packClient(data interface{}, f FileOpener) { //logging the client messages in JSON format
	jsonpackage, _ := json.Marshal(data) //converting to JSON format to make it standardized and easier to parse

	if _, err := f.clientFile.Write([]byte(jsonpackage)); err != nil { // writing the string to the file
		log.Fatal(err) // in case the function can't write print an error
	}

	if _, err := f.clientFile.Write([]byte("\r\n")); err != nil { // writing a new line for better visual
		log.Fatal(err)
	}
}

func packFlask(data interface{}, f FileOpener) { //logging the flask messages in JSON format
	jsonpackage, _ := json.Marshal(data)

	if _, err := f.flaskFile.Write([]byte(jsonpackage)); err != nil { //writing the data
		log.Fatal(err)
	}

	if _, err := f.flaskFile.Write([]byte("\r\n")); err != nil { //writing the new line
		log.Fatal(err)
	}
}

func openfile(pat string) FileOpener { // function used to open the files once in case the function is being
	// called in a loop, this would make the program not open file in
	// every loop, Hence improving the performance !
	t := time.Now()                         // getting the current time
	tim := t.Format("2006_01_02__15_04_05") // setting the format to YYYY_MM_DD__HH_MM_SS
	// visit https://stackoverflow.com/questions/20234104/how-to-format-current-time-using-a-yyyymmddhhmmss-format
	// if you want your own custom format

	path := pat + "/" + tim //setting the path for the folder with the time stamp

	if _, err := os.Stat(path); os.IsNotExist(err) { // if a folder doesn't exist with above specified path
		os.Mkdir(path, os.FileMode(os.ModePerm)) // create it
	}

	clientlogfile := path + "/dearclientlog.txt" //path to the client file in the folder. edit the string for your own custom file names
	flasklogfile := path + "/dearflasklog.txt"   //path to the flask file in the folder

	f, err := os.Create(clientlogfile) // create file if doesn't exist, which it should'nt because of time stamps
	check(err)

	f1, err := os.Create(flasklogfile) // create file if doesn't exist
	check(err)

	fileopener := FileOpener{clientFile: f, flaskFile: f1} // saving opened files in a struct to be used again without reopening
	return fileopener
}

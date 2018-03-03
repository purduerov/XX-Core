const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')
const url = require('url')
const fs = require('fs')
const ipc = electron.ipcMain


//port localhost:1905
//  ./pakfront/bin/russianword

//webpage gives arg and activates event
ipc.on('spawning', (event, arg) => {
  console.log(arg)
  //call function
  //check for error, log it below
  event.sender.send('Test Complete')
})

// ipc.on('listings', function(event) {
//
//   var names = Object;
//   fs.readdir('./settings/', function(err, files) {
//     if(err) {
//       throw err;
//     } else {
//       //console.log(files);
//       event.sender.send('list-reply', files);
//     }
//   });
// });

const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const url = require('url')
const fs = require('fs');
var spawn = require('child_process').spawn;

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
var cvbin = './pakfront/bin/';
var cvspawns = {};
var cvref = {};

let win


// ----------------------------------------------------------------------------------------
// Importing this adds a right-click menu with 'Inspect Element' option [worth it]
require('electron-context-menu')({
    prepend: (params, browserWindow) => [{
        label: 'Rainbow',
        // Only show it when right-clicking images
        visible: params.mediaType === 'image'
    }]
});
// ----------------------------------------------------------------------------------------

function createWindow() {
    // Create the browser window.
    win = new BrowserWindow({ width: 1600, height: 1200 })

    // and load the index.html of the app.
    win.loadURL(url.format({
        pathname: path.join(__dirname, 'frontend/main.html'),
        protocol: 'file:',
        slashes: true
    }))

    // Open the DevTools.
    win.webContents.openDevTools()

    // Emitted when the window is closed.
    win.on('closed', () => {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        win = null
    })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit()
    }
});

app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (win === null) {
        createWindow()
    }
});

ipcMain.on('find-files', (event) => {
  fs.readdir(cvbin, (err, files) => {
    files.forEach(file => {
      if (file.endsWith(".py")) {
        cvspawns[file.slice(0, -3)] = {'on': false};
      }
    });
    event.sender.send('files-found', cvspawns);
  });
});

ipcMain.on('cv-spawn', (event, file) => {
  if (!cvspawns[file].on) {
    console.log("Spawning")
    cvref[file] = spawn('python', [cvbin+file+'.py']);

    cvref[file].stdout.on('data', function(data) {
      console.log(data.toString());
    })
  } else {
    console.log("Killing")
    cvref[file].kill();
  }
  cvspawns[file].on = !cvspawns[file].on;


  event.sender.send('cv-spawned', {name: file, on: cvspawns[file].on, extra: cvref})
});


//this is the listener for the CV button press
ipcMain.on('spawn-event', (event, arg) => {
  console.log(arg);
  event.sender.send('spawn-reply', py);
  //The py function needs to be replaced with the cv process, and the address needs to be "require"d at the top

});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

var py = spawn('python', [cvbin + 'print.py']);

var data = [1, 2, 3, 4, 5, 6, 7, 8, 9];
var dataString = '';

/*Here we are saying that every time our node application receives data from the python process output stream(on 'data'), we want to convert that received data into a string and append it to the overall dataString.*/

py.stdout.on('data', function(data) {
    dataString = data.toString();
});

/*Once the stream is done (on 'end') we want to simply log the received data to the console.*/

py.stdout.on('end', function() {
    console.log('Sum of numbers=', dataString);
});

/*We have to stringify the data first otherwise our python process wont recognize it*/

py.stdin.write(JSON.stringify(data));

py.stdin.end();

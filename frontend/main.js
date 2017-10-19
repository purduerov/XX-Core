var packets = require("./src/packets.js");
let socketHost = `ws://raspberrypi.local:5000`;
let socket = io.connect(socketHost, {transports: ['websocket']});
let {shell, app, ipcRenderer} = window.require('electron');



// upon new data, save it locally
socket.on("dearclient", function(data) {    //Updates the data sent back from the server
    packets.dearclient = data;
});

// request new data
setInterval(() => {
    socket.emit("dearclient");
}, 50);

// send new data
setInterval(() => {             //Sends a message down to the server with updated surface info
    socket.emit("dearflask", packets.dearflask);
}, 50);

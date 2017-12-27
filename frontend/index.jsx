import React from 'react';
import {render} from 'react-dom';
import styles from './index.css';
import packet from './src/packets.js';
import Card from './src/components/Card.jsx';
import Cam_view from './src/components/Cam_View.jsx';
import Titlebar from './src/components/Titlebar.jsx';
import ThrusterInfo from './src/components/ThrusterInfo.jsx';

//var packets = require("./src/packets.js");
let socketHost = `ws://raspberrypi.local:5000`;
let socket = io.connect(socketHost, {transports: ['websocket']});
let {shell, app, ipcRenderer} = window.require('electron');

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = require("./src/packets.js"); //= $.extend(true, {}, packets);
  }

  render () {
    return (
      <div className="main">
          <div className="titlebar">
          <Titlebar/>
          </div>
          <div className="main-container">
              <div className="camera-width full-height center">
              </div>
              <div className="data-width full-height">
                  <div className="data-column">
                    <Card title="Thrusters">
                      <ThrusterInfo thrusters={this.state.dearclient.thrusters}/>
                    </Card>
                  </div>
                  <div className="data-column">
                  </div>
                  <div className="data-column">
                  </div>
              </div>
          </div>
      </div>
    );
  }

  componentDidMount() {
    var that = this;
    window.react = this;
    setInterval(function() {
      let all = that.state;
      all.dearclient.thrusters.forEach(function(key, i, arr) {
        arr[i] = Math.random();
      });

      that.setState(
        all
      );
    }, 3000);

    // upon new data, save it locally
    socket.on("dearclient", function(data) {    //Updates the data sent back from the server
        let all = that.state;
        all.dearclient = data;
        that.setState(
          all
        );
    });

    // request new data
    setInterval(() => {
        socket.emit("dearclient");
    }, 50);

    // send new data
    setInterval(() => {             //Sends a message down to the server with updated surface info
        socket.emit("dearflask", that.state.dearflask);
    }, 50);
  }
}

render(<App/>, document.getElementById('app'));
import React from 'react';
import {render} from 'react-dom';
import styles from './index.css';
import packet from './src/packets.js';
import Card from './src/components/Card.jsx';
import Cam_view from './src/components/CamView.jsx';
import Titlebar from './src/components/Titlebar.jsx';
import ThrusterInfo from './src/components/ThrusterInfo.jsx';
import ThrusterScales from './src/components/ThrusterScales.jsx';

//var packets = require("./src/packets.js");
let socketHost = `ws://raspberrypi.local:5000`;
let socket = io.connect(socketHost, {transports: ['websocket']});
let {shell, app, ipcRenderer} = window.require('electron');

let flaskcpy;
let confcpy;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = require("./src/packets.js"); //= $.extend(true, {}, packets);

    this.state.config = {
            version: 1.1, //INCREMENT IF YOU CHANGE THIS DATA STRUCTURE!
            thrust_scales: {
                master: 50, velX: 60, velY: 50,
                velZ: 60, pitch: 35,
                roll: 35, yaw: 25,
            },
            thrust_invert: {
                master: false, velX: false, velY: false,
                velZ: false, pitch: false,
                roll: false, yaw: false,
            },
            thruster_control: [   //invert is -1/1 for easy multiplication
                {power: 100, invert: 1}, {power: 100, invert: 1},
                {power: 100, invert: 1}, {power: 100, invert: 1},
                {power: 100, invert: 1}, {power: 100, invert: 1},
                {power: 100, invert: 1}, {power: 100, invert: 1}
            ],
            tool_scales: {
                claw: {
                    master: 50,
                    open: 50,
                    close: 50,
                    invert: 1
                },
                valve_turner: {
                    power: 30,
                    invert: 1
                },
                fountain_tool: {
                    power: 30,
                    invert: 1
                }
            }
        }

        
    flaskcpy = this.state.dearflask;
    confcpy = this.state.config;

    this.changeDisabled = this.changeDisabled.bind(this);
    this.changeThrustScales = this.changeThrustScales.bind(this);
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
                    <Card>
                      <ThrusterInfo thrusters={this.state.dearclient.thrusters}
                        disabled={this.state.dearflask.thrusters.disabled_thrusters}
                        rend={this.changeDisabled} />
                    </Card>
                  </div>
                  <div className="data-column">
                    <Card title="Thruster Control">
                      <ThrusterScales rend={this.changeThrustScales} 
                        scales={this.state.config.thruster_control}
                      />
                    </Card>
                  </div>
                  <div className="data-column">
                  </div>
              </div>
          </div>
      </div>
    );
  }

  changeDisabled(dis) {
    flaskcpy.thrusters.disabled_thrusters = dis;
    /*
    let all = this.state;
    flaskcpy.thrusters.disabled_thrusters.forEach(function(key, i) {
      if(key == 1) {
        all.dearclient.thrusters[i] = 0;
      }
    });
    */
    this.setState({
      dearflask: flaskcpy
    });
  }

  changeThrustScales(scales) {
    confcpy.thruster_control = scales;

    this.setState({
      config: confcpy
    });
  }

  componentDidMount() {
    var that = this;
    window.react = this;
    setInterval(function() {
      let all = that.state;                     //Edit copy, then update the state (one rerender initiated)
      all.dearclient.thrusters.forEach(function(key, i, arr) {    //for testing
        if(all.dearflask.thrusters.disabled_thrusters[i] === 0) {
          arr[i] = Math.random();
        } else {
          arr[i] = 0;
        }
      });

      that.setState(                            //Initiates rendering process
        all
      );
    }, 3000);

    // upon new data, save it locally
    socket.on("dearclient", function(data) {    //Updates the data sent back from the server
        that.setState(
          dearclient: data
        );
    });

    // request new data
    setInterval(() => {
        socket.emit("dearclient");
    }, 50);

    // send new data
    setInterval(() => {             //Sends a message down to the server with updated surface info
    /*
      let all = that.state;         //Edit copy, then update the state (one rerender initiated)
      all.dearflask = flaskcpy;
      all.inv = invcpy;

      that.setState(                //Let this interrupt change the state, fast enough
        all                         //Linearizes changes that should go unseen as well
      );
    */
      socket.emit("dearflask", that.state.dearflask);
    }, 50);
  }
}

render(<App/>, document.getElementById('app'));
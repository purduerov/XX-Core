import React from 'react';
import {render} from 'react-dom';
import styles from './index.css';
import packet from './src/packets.js';
import Seismograph from './src/components/Seismograph/Seismograph.jsx';
import CVview from './src/components/CVview/CVview.jsx'
import Card from './src/components/Card/Card.jsx';
import Cam_view from './src/components/CamView/CamView.jsx';
import ForceScales from './src/components/ForceScales/ForceScales.jsx'
import Titlebar from './src/components/Titlebar/Titlebar.jsx';
import ThrusterInfo from './src/components/ThrusterInfo/ThrusterInfo.jsx';
import ThrusterScales from './src/components/ThrusterScales/ThrusterScales.jsx';
import Gpinfo from './src/components/Gpinfo/Gpinfo.jsx';
import PacketView from './src/components/PacketView/PacketView.jsx';
import gp from './src/gamepad/bettergamepad.js';
import betterlayouts from './src/gamepad/betterlayouts.js';

//var packets = require("./src/packets.js");
let socketHost = `ws://localhost:5001`;

let socket = io.connect(socketHost, {transports: ['websocket']});
let {shell, app, ipcRenderer} = window.require('electron');

let flaskcpy;
let confcpy;


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = require("./src/packets.js"); //= $.extend(true, {}, packets);

    this.state.gp = require ("./src/gamepad/bettergamepad.js");

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
    this.changeForceScales = this.changeForceScales.bind(this);
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
                        rend={this.changeDisabled}
                      />
                    </Card>
                    <Card>
                    <PacketView packet={this.state.dearflask.thrusters.desired_thrust} />
                    </Card>
                  </div>
                  <div className="data-column">
                    <Card title="Directional Control">
                      <ForceScales rend={this.changeForceScales}
                        scales={this.state.config.thrust_scales}
                        />
                    </Card>
                  </div>
                  <div className="data-column">
                    <Card>
                      <Gpinfo buttons={this.state.gp.buttons}
                              ready={this.state.gp.ready}
                              axes={this.state.gp.axes}
                      />
                    </Card>
                    <Card title="Camera Vision Stats">
                      <CVview tdist={[40, 41, 42, 43, 44]} desc={"Fancy and great"}></CVview>
                    </Card>
                    <Card title="Seismograph">
                      <Seismograph
                        amplitude={this.state.dearclient.obs.seismograph_data.amplitude}
                        time={this.state.dearclient.obs.seismograph_data.time} >
                      </Seismograph>
                    </Card>
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

  changeForceScales(scales) {
    confcpy.thrust_scales = scales;

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

    setInterval(function() {
      if(gp.ready === false) {
//        console.log("not yet");
        gp.selectController();
      }
      if(gp.ready === true) {
        gp.update();
//        console.log('success');
      }

      that.setState( {                           //Initiates rendering process
        gp: gp }
      );
    }, 100);


    // upon new data, save it locally
    socket.on("dearclient", function(data) {    //Updates the data sent back from the server
        that.setState({
          dearclient: data
        });
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

import React from 'react';
import {render} from 'react-dom';
import styles from './index.css';
import packet from './src/packets.js';
import CVview from './src/components/CVview/CVview.jsx'
import ESCinfo from './src/components/ESCinfo/ESCinfo.jsx'
import Seismograph from './src/components/Seismograph/Seismograph.jsx';
import Card from './src/components/Card/Card.jsx';
import CameraScreen from './src/components/CameraScreen/CameraScreen.jsx';
import ForceScales from './src/components/ForceScales/ForceScales.jsx'
import Titlebar from './src/components/Titlebar/Titlebar.jsx';
import ThrusterInfo from './src/components/ThrusterInfo/ThrusterInfo.jsx';
import ThrusterScales from './src/components/ThrusterScales/ThrusterScales.jsx';
import Gpinfo from './src/components/Gpinfo/Gpinfo.jsx';
import PacketView from './src/components/PacketView/PacketView.jsx';
import betterlayouts from './src/gamepad/betterlayouts.js';

//var packets = require("./src/packets.js");
let socketHost = `ws://localhost:5001`;

let socket = io.connect(socketHost, {transports: ['websocket']});
let {shell, app, ipcRenderer} = window.require('electron');


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = require("./src/packets.js"); //= $.extend(true, {}, packets);

    this.state.gp = require ("./src/gamepad/bettergamepad.js");
    this.gp = require('./src/gamepad/bettergamepad.js');

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


    this.flaskcpy = this.state.dearflask;
    this.confcpy = this.state.config;

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
                <CameraScreen next={this.state.gp.buttons.left} prev={this.state.gp.buttons.right}></CameraScreen>
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
                      <Card>
                        <Gpinfo buttons={this.state.gp.buttons}
                                ready={this.state.gp.ready}
                                axes={this.state.gp.axes}
                                up={this.state.gp.up}
                                down={this.state.gp.down}
                        />
                      </Card>
                  </div>
                  <div className="data-column">
                    <Card title="Seismograph">
                      <Seismograph
                        amplitude={this.state.dearclient.sensors.obs.seismograph_data.amplitude}
                        time={this.state.dearclient.sensors.obs.seismograph_data.time} >
                      </Seismograph>
                    </Card>
                    <Card title="ESC readings">
                      <ESCinfo
                        currents={this.state.dearclient.sensors.esc.currents}
                        temp={this.state.dearclient.sensors.esc.temperatures}>
                      </ESCinfo>
                    </Card>
                    <Card title="CV view window">
                      <CVview desc={"We love Ben, yes we do"} tdist={[0.0, 0.1, 0.2, 0.4, 0.7, 0.8]} ></CVview>
                    </Card>
                  </div>
              </div>
          </div>
      </div>
    );
  }

  changeDisabled(dis) {
    this.flaskcpy.thrusters.disabled_thrusters = dis;
    /*
    let all = this.state;
    this.flaskcpy.thrusters.disabled_thrusters.forEach(function(key, i) {
      if(key == 1) {
        all.dearclient.thrusters[i] = 0;
      }
    });
    */
    this.setState({
      dearflask: this.flaskcpy
    });
  }

  changeThrustScales(scales) {
    this.confcpy.thruster_control = scales;

    this.setState({
      config: this.confcpy
    });
  }

  changeForceScales(scales) {
    this.confcpy.thrust_scales = scales;

    this.setState({
      config: this.confcpy
    });
  }

  componentDidMount() {
    var that = this;
    window.react = this;
    /*
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
    */

    setInterval(() => {
      if(this.gp.ready === false) {
//        console.log("not yet");
        this.gp.selectController();
      }
      if(this.gp.ready === true) {
        this.gp.update();
//        console.log('success');
      }

      that.setState( {                           //Initiates rendering process
        gp: this.gp }
      );
    }, 100);


    // upon new data, save it locally
    socket.on("dearclient", (data) => {    //Updates the data sent back from the server
        console.log(data)
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
      all.dearflask = this.flaskcpy;
      all.inv = invcpy;

      that.setState(                //Let this interrupt change the state, fast enough
        all                         //Linearizes changes that should go unseen as well
      );
    */
      that.state.dearflask.last_update = that.state.dearclient.last_update
        console.log(that.state.dearflask);
      socket.emit("dearflask", that.state.dearflask);
    }, 50);
  }
}

render(<App/>, document.getElementById('app'));

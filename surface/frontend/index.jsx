import React from 'react';
import {render} from 'react-dom';
import styles from './index.css';
import packet from './src/packets.js';
import CVview from './src/components/CVview/CVview.jsx'
import CrashZone from './src/components/CalculateCrashZone/CalculateCrashZone.jsx'
import ESCinfo from './src/components/ESCinfo/ESCinfo.jsx'
import Seismograph from './src/components/Seismograph/Seismograph.jsx';
import Card from './src/components/Card/Card.jsx';
import CameraScreen from './src/components/CameraScreen/CameraScreen.jsx';
import ForceScales from './src/components/ForceScales/ForceScales.jsx';
import Titlebar from './src/components/Titlebar/Titlebar.jsx';
import ThrusterInfo from './src/components/ThrusterInfo/ThrusterInfo.jsx';
import ThrusterScales from './src/components/ThrusterScales/ThrusterScales.jsx';
import Gpinfo from './src/components/Gpinfo/Gpinfo.jsx';
import ShowObject from './src/components/ShowObject/ShowObject.jsx'
import ToolView from './src/components/ToolView/ToolView.jsx';
import PacketView from './src/components/PacketView/PacketView.jsx';
import betterlayouts from './src/gamepad/betterlayouts.js';
import Spawn from './src/components/spawning/spawn.jsx';

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
            version: 1, //INCREMENT IF YOU CHANGE THIS DATA STRUCTURE!
            thrust_scales: {
                master: 50, velX: 100, velY: 100,
                velZ: 100, pitch: 100,
                roll: 100, yaw: 100,
            },
            thrust_invert: {
                master: 1, velX: 1, velY: 1,
                velZ: 1, pitch: 1,
                roll: 1, yaw: 1,
            },
            thruster_control: [   //invert is -1/1 for easy multiplication
                {power: 100, invert:  1}, {power: 100, invert:  1}, {power: 100, invert: -1}, {power: 100, invert:  1},
                {power: 100, invert:  1}, {power: 100, invert:  1}, {power: 100, invert:  1}, {power: 100, invert:  1}
            ],
            tool_scales: {
                manipulator: {
                    master: .25,
                    open: 1,
                    close: 1,
                    invert: 1
                },
                obs_tool: {   //unused, we're stepping it up and then down manually
                    master: .30,
                    invert: 1
                }
            }
        }


    this.flaskcpy = this.state.dearflask;
    this.clientcpy = this.state.dearclient;
    this.confcpy = this.state.config;

    this.changeDisabled = this.changeDisabled.bind(this);
    this.changeThrustScales = this.changeThrustScales.bind(this);
    this.changeForceScales = this.changeForceScales.bind(this);
    this.rendTools = this.rendTools.bind(this);
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
                        manipulator={this.state.dearflask.manipulator.power}
                        obs_tool={this.state.dearflask.obs_tool.power}
                        rend={this.changeDisabled}
                      />
                    </Card>
                    <Card title="CV Spawning">
                      <Spawn />
                    </Card>
                    <Card title="CV view window">
                      <CVview desc={"Purdo good, Purdon't let Eric make messages"} tdist={[0.0, 0.1, 0.2, 0.4, 0.7, 0.8]} ></CVview>
                    </Card>
                    <Card title="Crash Zone Calculator">
                      <CrashZone />
                    </Card>
                  </div>
                  <div className="data-column">
                    <Card title="Directional Control">
                      <ForceScales rend={this.changeForceScales}
                        scales={this.state.config.thrust_scales}
                        invert={this.state.config.thrust_invert}
                        />
                    </Card>
                    <Card title="Thruster Control">
                    	<ThrusterScales rend={this.changeThrustScales}
                    					scales={this.state.config.thruster_control}
                    					/>
                    </Card>
                    <Card>
                      <ToolView manipulator={this.state.dearflask.manipulator.power}
                                obs_tool={this.state.dearflask.obs_tool.power}
                                servo={this.state.dearflask.maincam_angle}
                                transmitter={this.state.dearflask.transmitter}
                                magnet={this.state.dearflask.magnet}
                                conf={this.state.config.tool_scales}
                                rend={this.rendTools}
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
                    <Card title="IMU">
                      <ShowObject obj={this.state.dearclient.sensors.imu} />
                    </Card>
                    <Card title="Pressure">
                      <ShowObject obj={this.state.dearclient.sensors.pressure} />
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

  rendTools(cinvcpy) {
    this.confcpy.tool_scales = cinvcpy;

    this.setState({
      config: this.confcpy
    })
  }

  changeThrustScales(scales) {
    this.confcpy.thruster_control = scales;

    this.confcpy.thruster_control.forEach((val, i) => {
      if(val.invert < 0) {
          this.flaskcpy.thrusters.inverted_thrusters[i] = -Math.abs(this.flaskcpy.thrusters.inverted_thrusters[i]);
      } else if (val.invert > 0) {
          this.flaskcpy.thrusters.inverted_thrusters[i] = Math.abs(this.flaskcpy.thrusters.inverted_thrusters[i]);
      } else {
        console.log("Thruster inversion value is 0... why???");
      }
    });

    this.setState({
      config: this.confcpy,
      dearflask: this.flaskcpy
    });
  }

  changeForceScales(scales, inv) {
    this.confcpy.thrust_scales = scales;
    this.confcpy.thrust_invert = inv;


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

      that.setState({                           //Initiates rendering process
        gp: this.gp,
        dearflask: this.flaskcpy
      });
    }, 100);


    // upon new data, save it locally
    socket.on("dearclient", (data) => {    //Updates the data sent back from the server
        //this.flaskcpy.last_update = data.last_update;
        this.clientcpy = data;
        //console.log(this.state.dearclient);
        //console.log(data);
        this.setState({
          dearclient: this.clientcpy
        });
    });

    // request new data
    setInterval(() => {
        socket.emit("dearclient");
    }, 50);

    // send new data
    setInterval(() => {             //Sends a message down to the server with updated surface info
      //console.log(that.state.dearflask);
      socket.emit("dearflask", that.state.dearflask);
    }, 50);
  }
}

render(<App/>, document.getElementById('app'));

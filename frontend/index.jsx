import React from 'react';
import {render} from 'react-dom';
import styles from './index.css';
import packet from './src/packets.js';
import Card from './src/components/Card.jsx';
import Cam_view from './src/components/Cam_View.jsx';
import Titlebar from './src/components/Titlebar.jsx';
import ThrusterInfo from './src/components/ThrusterInfo.jsx';
import ThrusterScales from './src/components/ThrusterScales.jsx';

//var packets = require("./src/packets.js");
let socketHost = `ws://raspberrypi.local:5000`;
let socket = io.connect(socketHost, {transports: ['websocket']});
let {shell, app, ipcRenderer} = window.require('electron');

let flaskcpy;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = require("./src/packets.js"); //= $.extend(true, {}, packets);
    flaskcpy = this.state.dearflask;

    //this.changeFlask = this.changeFlask.bind(this);   //bind App's `this` to changeFlask()
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
                      <ThrusterInfo thrusters={this.state.dearclient.thrusters}/>
                    </Card>
                  </div>
                  <div className="data-column">
                    <Card title="Thruster Control">
                      <ThrusterScales rend={this.changeThrustScales} 
                        scales={this.state.dearflask.thrusters.thruster_scales}
                        onoff={this.state.dearflask.thrusters.disabled_thrusters} />
                    </Card>
                  </div>
                  <div className="data-column">
                  </div>
              </div>
          </div>
      </div>
    );
  }

  changeThrustScales(val, dis) {
    let all = this.state;
    flaskcpy.thruster_scales = val;
    flaskcpy.disabled_thrusters = dis;
  }

  changeFlask(desired) {
    flaskcpy = desired;     //If component changes this, rerender is unnecessary
  }                          //could possibly take out rerendering & just send flaskcpy...

  componentDidMount() {
    var that = this;
    window.react = this;
    setInterval(function() {
      let all = that.state;                     //Edit copy, then update the state (one rerender initiated)
      all.dearclient.thrusters.forEach(function(key, i, arr) {    //for testing
        arr[i] = Math.random();
      });

      that.setState(                            //Initiates rendering process
        all
      );
    }, 3000);

    // upon new data, save it locally
    socket.on("dearclient", function(data) {    //Updates the data sent back from the server
        let all = that.state;                   //Edit copy, then update the state (one rerender initiated)
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
      let all = that.state;         //Edit copy, then update the state (one rerender initiated)
      all.dearflask = flaskcpy;

      that.setState(                //Let this interrupt change the state, fast enough
        all                         //Linearizes changes that should go unseen as well
      );

      socket.emit("dearflask", that.state.dearflask);
    }, 50);
  }
}

render(<App/>, document.getElementById('app'));
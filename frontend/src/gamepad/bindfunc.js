/*
button template:
  btn: {
    value: {
      params: undefined,
      func: null,
    },
    press: {
      params: undefined,
      func: null,
    },
    release: {
      params: undefined,
      func: null,
    },
  },

axes template:
  side: {
      params: undefined,
      func: null,
        },

        // a:{
        //   value: {
        //     func: function() {
        //       react.state.dearflask.thrusters.desired_thrust = gp.buttons.a.curVal
        //     }
        //   },
        // },
        // up: {
        //   press: {
        //     func: function() {
        //       react.state.dearflask.thrusters.desired_thrust =
        //     }
        //
        //   },
        //   release: {
        //
        //   },
        // },

  */

//import gp from './bettergamepad.js';
//var packets = require('./src/packets.js')

var bind = {
  btn:{
    lb:{ //roll counterclockwise
      press: {
        func: function() {
          react.state.dearflask.thrusters.desired_thrust[3] = -react.state.gp.buttons.lb.curVal;
        },
      },
      release: {
        func: function() {
          if(react.state.dearflask.thrusters.desired_thrust[3] < 0) {
            react.state.dearflask.thrusters.desired_thrust[3] = 0;
          }
        },
      },
    },
    rb:{ //roll clockwise
      press: {
        func: function() {
          react.state.dearflask.thrusters.desired_thrust[3] = react.state.gp.buttons.rb.curVal;
        },
      },
      release: {
        func: function() {
          if(react.state.dearflask.thrusters.desired_thrust[3] > 0) {
            react.state.dearflask.thrusters.desired_thrust[3] = 0;
          }
        },
      },
    },
    ltrigger:{ //descend
      press: {
        func: function() {
          react.state.dearflask.thrusters.desired_thrust[2] = -react.state.gp.buttons.ltrigger.curVal;
        },
      },
      release: {
        func: function() {
          if(react.state.dearflask.thrusters.desired_thrust[2] < 0) {
            react.state.dearflask.thrusters.desired_thrust[2] = 0;
          }
        },
      },
    },
    rtrigger:{ //ascend
      press: {
        func: function() {
          react.state.dearflask.thrusters.desired_thrust[2] = react.state.gp.buttons.rtrigger.curVal;
        },
      },
      release: {
        func: function() {
          if(react.state.dearflask.thrusters.desired_thrust[2] > 0) {
            react.state.dearflask.thrusters.desired_thrust[2] = 0;
          }
        },
      },
    },

  }, //end btn

  axes: {
    LstickXaxis: {
      func: function() {
        react.state.dearflask.thrusters.desired_thrust[1] = react.state.gp.axes.LstickXaxis.curVal;
      }
    },
    LstickYaxis: {
      func: function() {
        react.state.dearflask.thrusters.desired_thrust[0] = -react.state.gp.axes.LstickYaxis.curVal;
      }
    },
    RstickXaxis: {
      func: function() {
        react.state.dearflask.thrusters.desired_thrust[5] = react.state.gp.axes.RstickXaxis.curVal;
      }
    },
    RstickYaxis: {
      func: function() {
        react.state.dearflask.thrusters.desired_thrust[4] = -react.state.gp.axes.RstickYaxis.curVal;
      }
    },
  },

  activate: function() {
    Object.keys(bind).forEach(function(btn_ax, i) {  //goes through btn or ax
      if(btn_ax != "activate") {
        Object.keys(bind[btn_ax]).forEach(function(piece, j) { //goes through buttons or left and right axes
          Object.keys(bind[btn_ax][piece]).forEach(function(which, k) {  //goes through the individual functions
            //console.log(btn_ax+": "+piece+", "+which);
            gp[btn_ax+"_bind"](piece, which, bind[btn_ax][piece][which].func);
          });
        });
      }
    });
  }

}; //end bind
module.exports = bind;
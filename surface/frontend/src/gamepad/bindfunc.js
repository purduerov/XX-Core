/*
button template:
  btn: {
    value: {
      params: undefined,
      func: null,
    },
    pressed: {
      params: undefined,
      func: null,
    },
    released: {
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
        //       react.flaskcpy.thrusters.desired_thrust = gp.buttons.a.curVal
        //     }
        //   },
        // },
        // up: {
        //   pressed: {
        //     func: function() {
        //       react.flaskcpy.thrusters.desired_thrust =
        //     }
        //
        //   },
        //   released: {
        //
        //   },
        // },

  */

var bind = {
  btn:{
    lb:{ //roll counterclockwise
      pressed: {
        func: function() {
          var stuff = react.state.config.thrust_scales;
          react.flaskcpy.thrusters.desired_thrust[3] = -react.gp.buttons.lb.curVal * stuff.master * stuff.roll / 10000;
        },
      },
      released: {
        func: function() {
          if(react.flaskcpy.thrusters.desired_thrust[3] < 0) {
            react.flaskcpy.thrusters.desired_thrust[3] = 0;
          }
        },
      },
    },
    rb:{ //roll clockwise
      pressed: {
        func: function() {
          var stuff = react.state.config.thrust_scales;
          react.flaskcpy.thrusters.desired_thrust[3] = react.gp.buttons.rb.curVal * stuff.master * stuff.roll / 10000;
        },
      },
      released: {
        func: function() {
          if(react.flaskcpy.thrusters.desired_thrust[3] > 0) {
            react.flaskcpy.thrusters.desired_thrust[3] = 0;
          }
        },
      },
    },
    rb:{ //close manipulator
      press: {
        func: function() {
          react.state.dearflask.manipulator = react.state.gp.buttons.rb.curVal * .3;
        },
      },
      release: {
        func: function() {
          if(react.state.dearflask.manipulator > 0) {
            react.state.dearflask.manipulator = 0;
          }
        },
      },
    },
    lb:{ //open manipulator
      press: {
        func: function() {
          react.state.dearflask.manipulator = react.state.gp.buttons.lb.curVal * .3 * -1;
        },
      },
      release: {
        func: function() {
          if(react.state.dearflask.manipulator < 0) {
            react.state.dearflask.manipulator = 0;
          }
        },
      },
    },
    rpress: { //obs leveler power forwards
      press: {
        func: function() {
          react.state.dearflask.obs_tool = react.state.gp.buttons.rpress.curVal * .3;
        },
      },
      release: {
        func: function() {
          if(react.state.dearflask.obs_tool > 0) {
            react.state.dearflask.obs_tool = 0;
          }
        },
      },
    },
    lpress: { // obs leveler power backwards
      press: {
        func: function() {
          react.state.dearflask.obs_tool = react.state.gp.buttons.lpress.curVal * -1 * .3;
        },
      },
      release: {
        func: function() {
          if(react.state.dearflask.obs_tool > 0) {
            react.state.dearflask.obs_tool = 0;
          }
        },
      },
    },

  }, //end btn

  axes: {
    LstickXaxis: {
      curVal: {
        func: function() {
          var stuff = react.state.config.thrust_scales;
          react.flaskcpy.thrusters.desired_thrust[1] = react.gp.axes.LstickXaxis.curVal * stuff.master * stuff.velY / 10000;
        }
      }
    },
    LstickYaxis: {
      curVal: {
        func: function() {
          var stuff = react.state.config.thrust_scales;
          react.flaskcpy.thrusters.desired_thrust[0] = -react.gp.axes.LstickYaxis.curVal * stuff.master * stuff.velX / 10000;
        }
      }
    },
    RstickXaxis: {
      curVal: {
        func: function() {
          var stuff = react.state.config.thrust_scales;
          react.flaskcpy.thrusters.desired_thrust[5] = react.gp.axes.RstickXaxis.curVal * stuff.master * stuff.yaw / 10000;
        }
      }
    },
    RstickYaxis: {
      curVal: {
        func: function() {
          var stuff = react.state.config.thrust_scales;
          react.flaskcpy.thrusters.desired_thrust[4] = -react.gp.axes.RstickYaxis.curVal * stuff.master * stuff.pitch / 10000;
        }
      }
    },
    /*
      THESE ARE A DELICATE BALANCE
      Only change the weird up/down referencing if you've REALLY thought through what you're doing
      I spent too much time on this late at night when I would have rather been at the cactus.
      Please don't make it for naught...
      -- Ian

      Allows for the last trigger pressed to take dominace over whether the ROV is going up, or down
    */
    Ltrigger: { //descend
      curVal: {
        func: function() {
          var stuff = react.state.config.thrust_scales;
          if(react.gp.axes.Ltrigger.curVal != 0) {
            if(react.gp.up < 2) {
              console.log(react.gp.axes.Ltrigger.curVal+" "+stuff.master+" "+stuff.velZ);
              react.flaskcpy.thrusters.desired_thrust[2] = -react.gp.axes.Ltrigger.curVal * stuff.master * stuff.velZ / 10000;
              react.gp.down = 1 + react.gp.up
            }
          } else {
            react.gp.down = 0;
          }
          if(react.gp.down == react.gp.up) {
            react.flaskcpy.thrusters.desired_thrust[2] = 0;
          }
        }
      }
    },
    Rtrigger: { //ascend
      curVal: {
        func: function() {
          var stuff = react.state.config.thrust_scales;
          if(react.gp.axes.Rtrigger.curVal != 0) {
            if(react.gp.down < 2) {
                react.flaskcpy.thrusters.desired_thrust[2] = react.gp.axes.Rtrigger.curVal * stuff.master * stuff.velZ / 10000;
                react.gp.up = 1 + react.gp.down
            }
          } else {
            react.gp.up = 0;
          }
          if(react.gp.down == react.gp.up) {
            react.flaskcpy.thrusters.desired_thrust[2] = 0;
          }
        }
      }
    },
  },

  activate: function(gp) {
    //console.log(gp)
    Object.keys(bind).forEach(function(btn_ax, i) {  //goes through btn or ax
      if(btn_ax != "activate") {
        Object.keys(bind[btn_ax]).forEach(function(piece, j) { //goes through buttons or left and right axes
          Object.keys(bind[btn_ax][piece]).forEach(function(which, k) {  //goes through the individual functions
            //console.log(btn_ax+"_bind: "+piece+", "+which);
            gp[btn_ax+"_bind"](piece, which, bind[btn_ax][piece][which].func);
          });
        });
      }
    });
  }

}; //end bind
module.exports = bind;

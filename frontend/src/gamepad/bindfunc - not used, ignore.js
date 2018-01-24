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

  */

let gp = require('./bettergamepad.js')
let react = {
  dearclient: {
    IMU: {
      x: 0,
      y: 0,
      z: 0,
      roll: 0,
      pitch: 0,
      yaw: 0,
    }
  }
}

var bind = {
  btn:{
    a:{
      change: {

      },
    },
    b: {
      change: {

      },
    },
    x: {
      change: {

      },
    },
    y: {
      change:{

      },
    },
    up: {
      press: {

      },
      release: {

      },
    },
    down: {
      press: {

      },
      release: {

      },
    },
    left: {
      press: {

      },
      release: {

      },
    },
    right: {
      press: {

      },
      release: {

      },
    },

  axis: {
    leftx: {

    },
    lefty: {

    },
    rightx: {

    },
    righty: {

    },
  },



} //end bind

//writing the object that cancerous aids will call from

//make loop that wants to check id and bind keys if it matches
var layouts = {
  rock: {
    "idMatch": ["Some other gamepad with the same mapping", "Xbox 360 Controller (XInput STANDARD GAMEPAD)"],
    "buttons" : [        //array
    {"indx": 0, "name": "a", "pressed": 1, "notpressed": 0, "where": "buttons"},        //object in array
    {"indx": 1, "name": "b", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 2, "name": "x", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 3, "name": "y", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 4, "name": "lb", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 5, "name": "rb", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 6, "name": "ltrigger", "pressed": 1, "notpressed": 0, "where": "buttons"}, //will be axis in another os
    {"indx": 7, "name": "rtrigger", "pressed": 1, "notpressed": 0, "where": "buttons"}, //will be axis in another os
    {"indx": 8, "name": "select", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 9, "name": "start", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 10, "name": "lpress", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 11, "name": "rpress", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 12, "name": "up", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 13, "name": "down", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 14, "name": "left", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 15, "name": "right", "pressed": 1, "notpressed": 0, "where": "buttons"}
  ],
    "axes" : [
    {"indx": 0, "name": "LstickXaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
    {"indx": 0, "name": "LstickYaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
    {"indx": 0, "name": "RstickXaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
    {"indx": 0, "name": "RstickYaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},  //6,7 joysticks
  ]
  },

  elite: {
    "idMatch": ["Not your mother's xbox Controller"],
    "buttons" : [],
    "axes" : []
  }
}

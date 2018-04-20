//writing the object that cancerous aids will call from

//make loop that wants to check id and bind keys if it matches

global.layouts = {
  rock: {
    "idMatch": ["Some other gamepad with the same mapping", "Xbox 360 Controller (XInput STANDARD GAMEPAD)"],
    "buttons" : [        //array
    {"indx": 0, "name": "a", "pressed": 1, "notpressed": 0, "where": "buttons"},        //object in array
    {"indx": 1, "name": "b", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 2, "name": "x", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 3, "name": "y", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 4, "name": "lb", "pressed": 1, "notpressed": 0, "where": "buttons"},
    {"indx": 5, "name": "rb", "pressed": 1, "notpressed": 0, "where": "buttons"},
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
    {"indx": 1, "name": "LstickYaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
    {"indx": 2, "name": "RstickXaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
    {"indx": 3, "name": "RstickYaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},  //6,7 joysticks
    //These will be axes, but are in buttons for navigator.getGamepads()
    {"indx": 6, "name": "Ltrigger", "min": 0, "max": 1, "where": "buttons", "constant": 0}, //will be axis in another os
    {"indx": 7, "name": "Rtrigger", "min": 0, "max": 1, "where": "buttons", "constant": 0}, //will be axis in another os
    ]
  },

  elite: {
    "idMatch": ["Not your mother's xbox Controller"],
    "buttons" : [],
    "axes" : []
  },

  LinuxRock: {
    "idMatch": ["Performance Designed Products Rock Candy Gamepad for Xbox 360 (Vendor:"],
    "buttons": [
      {"indx": 0, "name": "a", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 1, "name": "b", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 2, "name": "x", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 3, "name": "y", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 4, "name": "lb", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 5, "name": "rb", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 6, "name": "select", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 7, "name": "start", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 8, "name": "home", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 9, "name": "lpress", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 10, "name": "rpress", "pressed": 1, "notpressed": 0, "where": "buttons"},
      //These will be buttons for gp, but are in axes for navigator.getGamepads()
      {"indx": 7, "name": "up", "pressed": -1, "notpressed": 0, "where": "axes"},
      {"indx": 7, "name": "down", "pressed": 1, "notpressed": 0, "where": "axes"},
      {"indx": 6, "name": "left", "pressed": -1, "notpressed": 0, "where": "axes"},
      {"indx": 6, "name": "right", "pressed": 1, "notpressed": 0, "where": "axes"}
    ],
    "axes": [
      {"indx": 0, "name": "LstickXaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
      {"indx": 1, "name": "LstickYaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
      {"indx": 2, "name": "Ltrigger", "min": -1,"max": 1, "where": "axes", "constant": 0},
      {"indx": 3, "name": "RstickXaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
      {"indx": 4, "name": "RstickYaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
      {"indx": 5, "name": "Rtrigger", "min": -1,"max": 1, "where": "axes", "constant": 0},
    ]
  },

  LinuxOne : {
    "idMatch": ["Microsoft Controller (STANDARD GAMEPAD Vendor:"],
    "buttons": [
      {"indx": 0, "name": "a", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 1, "name": "b", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 2, "name": "x", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 3, "name": "y", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 4, "name": "lb", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 5, "name": "rb", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 8, "name": "select", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 9, "name": "start", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 10, "name": "lpress", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 11, "name": "rpress", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 12, "name": "up", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 13, "name": "down", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 14, "name": "left", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 15, "name": "right", "pressed": 1, "notpressed": 0, "where": "buttons"},
      {"indx": 16, "name": "home", "pressed": 1, "notpressed": 0, "where": "buttons"}
    ],
    "axes": [
      {"indx": 0, "name": "LstickXaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
      {"indx": 1, "name": "LstickYaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
      {"indx": 2, "name": "RstickXaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
      {"indx": 3, "name": "RstickYaxis", "min": -1,"max": 1, "where": "axes", "constant": 0},
      {"indx": 6, "name": "Ltrigger", "min": 0,"max": 1, "where": "buttons", "constant": 0},
      {"indx": 7, "name": "Rtrigger", "min": 0,"max": 1, "where": "buttons", "constant": 0},
    ]
  }
}

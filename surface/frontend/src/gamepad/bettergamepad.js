require("./betterlayouts.js");
var bind = require('./bindfunc.js')

var gp = {
  buttons:  {},
  axes:     {},
  prev_but: {},
  selID: 0,
  select: function(rate) {  //prints id of activated gamepad
    gp.selID = setInterval(gp.selectController, rate);
  },
  gamepadIndex: -1, //the index that goes with navigator.getGamepads
  layoutKey: -1, //the name of the controller
  ready: false,

  selectController: function() {
    var cur = navigator.getGamepads();
    Object.keys(cur).forEach(function(key, i) {
      if (key !="length") {
        if (cur[key] != null) {
          if(cur[key].buttons[1] != undefined) {
            cur[key].buttons.forEach(function(key_b, i) {
              if (cur[key].buttons[i].pressed){
                //console.log(cur[key].id);
                gp.map(key, cur[key].id);
              }
            });
          }
        }
      }
    });
  },

  map: function(key, id) { //id is the id in chrome driver
    var b = 10;  //random number of possible ids, not important
    Object.keys(layouts).forEach(function(key_gp, i_gp) {
      for(var a = 0; a < b; a++) {   //loops through ids of betterlayouts
        if(layouts[key_gp].idMatch[a] == id) {    //For loop through idMatch rather than using just the first one
          b = a;
          gp.ready = true;
          clearInterval(gp.selID);
          gp.selID = -1;
          for(var j = 0; j < layouts[key_gp].buttons.length; j++) {
            gp.buttons[layouts[key_gp].buttons[j].name] = {pressed: 0, released: 0, curVal: 0};
            gp.prev_but[layouts[key_gp].buttons[j].name] = 0;
            //console.log(layouts[key_gp].buttons[j].name+": "+gp.buttons[layouts[key_gp].buttons[j].name].pressed); //eventually remove
          }
            gp.gamepadIndex = key;
            gp.layoutKey = key_gp;
            bind.activate;
            gp.zero();
        }
      }
    });
  },
// update doesn't have a function call yet

 update: function() {
   var cur = navigator.getGamepads();
   //console.log(layouts[gp.layoutKey]);
   for(var index = 0; index < layouts[gp.layoutKey].buttons.length; index++)
   {
     gp.buttons[layouts[gp.layoutKey].buttons[index].name].curVal = cur[gp.gamepadIndex].buttons[index].value;
     gp.pressRelease(layouts[gp.layoutKey].buttons[index].name);

     name = layouts[gp.layoutKey].buttons[index].name;

     if(bind.btn[name]) {
       if(bind['btn'][name]['press'].func && gp.buttons[name].pressed) {    //runs bindfunc
          bind['btn'][name]['press'].func();
       }

       if(bind['btn'][name]['release'].func && gp.buttons[name].released) {
          bind['btn'][name]['release'].func();
       }
     }
   }
   for(var index_2 = 0; index_2 < layouts[gp.layoutKey].axes.length; index_2++)
   {
     name = layouts[gp.layoutKey].axes[index_2].name;
     if(.1 < Math.abs(gp.adjust(index_2))) {
       gp.axes[layouts[gp.layoutKey].axes[index_2].name].curVal = gp.adjust(index_2);
     } else {
       gp.axes[layouts[gp.layoutKey].axes[index_2].name].curVal = 0;
     }
     if (bind['axes']) { //runs bindfunc
       bind['axes'][name].func();
     }
   }
 },

 pressRelease: function(but_name) {
   //console.log(but_name);
   if(gp.prev_but[but_name] < gp.buttons[but_name].curVal) {
     //console.log("pres");
     gp.buttons[but_name].pressed = 1;
     gp.buttons[but_name].released = 0;
   } else if (gp.prev_but[but_name] > gp.buttons[but_name].curVal) {
     //console.log(" rel");
     gp.buttons[but_name].released = 1;
     gp.buttons[but_name].pressed = 0;
   } else {
     gp.buttons[but_name].released = 0;
     gp.buttons[but_name].pressed = 0;
   }
   gp.prev_but[but_name] = gp.buttons[but_name].curVal;
 },

 zero: function() {  //gets values of constants
   var cur = navigator.getGamepads();
   for(var j = 0; j < layouts[gp.layoutKey].axes.length; j++) {  //initializes the array for each axis
     gp.axes[layouts[gp.layoutKey].axes[j].name] = {changed: 0, curVal: 0, constant: 0, past: 0};
   }

   for(var index = 0; index < layouts[gp.layoutKey].axes.length; index++) //copy of the function in update, but sets constants
   {
     gp.axes[layouts[gp.layoutKey].axes[index].name].constant = cur[gp.gamepadIndex].axes[index];
   }
 },

 adjust: function(index_2) {
   var cur = navigator.getGamepads();
   let newVal = cur[gp.gamepadIndex].axes[index_2] - gp.axes[layouts[gp.layoutKey].axes[index_2].name].constant;
   if (newVal > 0) {
     newVal = (newVal / (1 - gp.axes[layouts[gp.layoutKey].axes[index_2].name].constant));
   }
   else if (newVal < 0) {
     newVal = newVal / (1 + gp.axes[layouts[gp.layoutKey].axes[index_2].name].constant);
   }
   return(newVal);
 }

//this.bindbtn = function() {    < if I want to go this route, but seems redundant
// },

}//end gp
//gp.select(50);
module.exports = gp;

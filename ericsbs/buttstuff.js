
var refreshIntervalID = setInterval(print, 200);

function print () {
  var cur = navigator.getGamepads();
  Object.keys(cur).forEach(function(key, i) {
    if (key !="length") {
      if (cur[key] != null) {
        if (cur[key].id != "Unknown Gamepad (Vendor: 06cb Product: 0ac3)") {
          if (cur[key].buttons != undefined){
            Object.keys(cur[key].buttons).forEach(function(key_b, i) {
              if (cur[key].buttons[i].pressed != false){
                console.log(i);
                console.log(cur[key].id);
                clearInterval(refreshIntervalID);
              }
            });
          }
        }
      }
    }
  });
}

print();

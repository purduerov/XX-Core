var active_div = function() {
  var div = $("#moving");
  var info = $("#info");
  var txt = "";
  if(gp.buttons.a.curVal && !gp.buttons.b.curVal) {
      div.css("background-color", "cyan");
  } else if(gp.buttons.b.curVal && !gp.buttons.a.curVal) {
      div.css("background-color", "red");
  }

  if(gp.buttons.y.curVal && !gp.buttons.x.curVal) {
      div.height("+=2");
      div.width("+=2");
      div.css({top: "-=1"});
      div.css({left: "-=1"});
  } else if(gp.buttons.x.curVal && !gp.buttons.y.curVal) {
      div.height("-=2");
      div.width("-=2");
      if(parseInt(div.width()) != 0) {
          div.css({top: "+=1"});
          div.css({left: "+=1"});
      }
  }

  if(gp.buttons.up.pressed) {
    div.css({top: "0"});
  }
  if(gp.buttons.down.released) {
    div.css({top: "100%"});
    div.css({top: "-="+(div.height()+3)});
  }
  if(gp.buttons.left.pressed) {
    div.css({left: "0"});
  }
  if(gp.buttons.right.released) {
    div.css({left: "100%"});
    div.css({left: "-="+(div.width()+3)});
  }



  div.css({top: "+="+parseInt(10*gp.axes.LstickYaxis.curVal)+"px"});
  div.css({left: "+="+parseInt(10*gp.axes.LstickXaxis.curVal)+"px"});


  Object.keys(gp.buttons) .forEach(function(key_b, i) {
    if(key_b != "length"){
      txt = txt+"</br>"+key_b+": "+(gp.buttons[key_b].curVal);
      //console.log("Buttons: "+gp.buttons[key_b].curVal+" "+key_b);
    }
  });
  Object.keys(gp.axes).forEach(function(key_a, i) {
    if(key_a != "length"){
        txt = txt+"</br>"+key_a+"</br><p>"+(gp.axes[key_a].curVal)+"</p>";
        //console.log("Axes: "+gp.axes[key_a]+" "+key_a);
/*        if(key_a == "right") {
          txt = txt + "</br></br> x - x-off: " + (navigator.getGamepads()[gp.i_use].axes[layouts[gp.layout].axes[key_a].x])
                    + "</br> 1 - x-off: " + (1 - gp.getDisplace().right.x);

        }
*/      }
  });

  info.html(txt);
}

var go1 = -1;
var go2 = -1;

var run = function(abt) {
  if(gp.ready) {
    window.clearInterval(go1);
    go1 = -1;
    go2 = window.setInterval(function() {
      gp.update();  //used to be get_current
      if(gp.ready) {
        active_div();
      } else {
        $("#reset").click();
      }
    }, 10);
  }
}

$(document).ready(function() {
  var abt = $("#titles");
  gp.selectController(abt);  //used to be gp.set

  go1 = window.setInterval(function() { run(abt); }, 50);

  $("#reset").click(function() {
    if(go2 != -1) {
      gp.ready = false;
      window.clearInterval(go2);
    } else {console.log("go2: "+go2+" go1: "+go1);}
    $("#info").empty();
    gp.set(abt);
    go1 = window.setInterval(function() { run(abt); }, 50);
  });

  $("#bind").click(function() {
    gp.bind("a", "press", function(arg) { arg.message.html("Re-link, </br>\'"+arg.btn+"\' says hi "+arg.count+" times!"); arg.count += 1; },
            {message: $("#reset"), btn: "a", count: 0});
  });
});

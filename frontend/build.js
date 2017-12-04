/*
 *  Compiler Version 1.0
 *  REQUIRES a main.[js, css, html] to be within the same scope of build.js
 *  A lone flag of #html-compiler:~component_name~ is needed to insert a component
 *  All components expected to be in frontend/src/components/
 */

var fs = require('fs');

var finals = "src/elec_finals/final"

var workorder = ["main"];
var offset = -1;
var top = "./main";

function html_fill(filename, whitespace, spot) {
  //open and read file line by line
  var html = fs.readFileSync(filename, {encoding: 'utf8'});
  html = html.split('\n');


  let present = false;    //if true, can't index like normal
  for(let i = 0; i < html.length; i++) {
    let input = html[i].search("#html-compiler");
    if(input != -1) {
      let space = "";
      for(let j = 0; j < input; j++) {
        space += " ";
      }
      let file = html[i].slice(input+15);

      if(workorder.indexOf(file) == -1) {
        workorder.push(file);
      }

      let my_html = "".concat("src/components/", file, "/", file, ".html");
      let data = fs.readFileSync("src/components/"+file+"/"+file+".html", {encoding: 'utf8'});
      data = data.split('\n');

      html.splice(i, 1);
      for(let j = 0; j < data.length; j++) {
        if(data[j] != '')  {        //if readability needed for debugging, comment this out
          //console.log("empty");
        //} else {
          html.splice(i+j, 0, space+data[j]);
        }
      }
      i--;
    }
  }
  html = html.join('\n');

  fs.writeFile(finals+".html", html, function(err) {
    if(err) {
      throw err;
    }
  });
}

function js_css_add() {
  var css = finals+".css";
  var js = finals+".js";

  fs.truncateSync(js, 0);
  fs.truncateSync(css, 0);

  console.log(workorder);

  var my_files = "";

  for(var i = 0; i < workorder.length; i++) {
    console.log(i != 0);
    if(i != 0) {
      console.log("comp");
      my_files = "".concat("src/components/", workorder[i], "/", workorder[i]);
    } else {
      console.log("main");
      my_files = workorder[i];
    }

    let data = fs.readFileSync(my_files+".js", {encoding: 'utf8'});
    fs.appendFileSync(js, data);

    data = fs.readFileSync(my_files+".css", {encoding: 'utf8'});
    fs.appendFileSync(css, data);
  }
}

function make_files() {
  html_fill(top+".html", 0, 0);
  js_css_add();
}

make_files();

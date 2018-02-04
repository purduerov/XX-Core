const fs = require('fs');
var packets = require('/home/zhukov/Projects/rov/XX-Core/frontend/src/packets.js')

var pak = {"dearflask": packets.dearflask,
	   "dearclient":packets.dearclient};
 var jsonObj = JSON.stringify(pak);
 console.log(jsonObj);
  
// stringify JSON Object
 var jsonContent = JSON.stringify(jsonObj);
 console.log(jsonContent);
   
 fs.writeFile("packets.json", jsonContent, 'utf8', function (err) {
 if (err) {
   console.log("An error occured while writing JSON Object to File.");
   return console.log(err);
   }
                            
  console.log("JSON file has been saved.");
});

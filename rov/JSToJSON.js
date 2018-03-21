const fs = require('fs');
var srcdir = process.argv[2]
var outdir = process.argv[3]
var packets = require(srcdir + 'packets.js')

var pak = {"dearflask": packets.dearflask,
	   "dearclient":packets.dearclient};
 var jsonObj = JSON.stringify(pak);
   
 fs.writeFile(outdir + "packets.json", jsonObj, 'utf8', function (err) {
 if (err) {
   console.log("An error occured while writing JSON Object to File.");
   return console.log(err);
   }
                            
  console.log("JSON file has been saved.");
});

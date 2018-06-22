const math = require('mathjs');
/*
var heading = 184;
var Aairspeed = 93;
var ascentRate = 10;
var failure = 43;
var Dairspeed = 64;
var descentRate = 6;
var Wheading = 270 - 180;

//console.log(JSON.stringify({ heading: 0, Aairspeed: 0, ascent: 0, failure: 0, Dairspeed: 0, descentRate: 0, Wheading: 0 }))
//console.log(process.argv)
//console.log(process.argv.length)
*/
try {
    args = JSON.parse(process.argv[2]);

    //console.log(typeof args);
    //console.log(args.heading);

    //console.log(args);

    var inc = 0.01;
    var equation = "(" + args.equation + ")" + inc;

    var heading = args.heading
    var Aairspeed = args.Aairspeed
    var ascentRate = args.ascentRate
    var failure = args.failure
    var Dairspeed = args.Dairspeed
    var descentRate = args.descentRate
    var Wheading = args.Wheading > 180 ? args.Wheading - 180 : args.Wheading + 180;

    var time = failure;

    var radiusA = Aairspeed * failure;
    var ya = radiusA * Math.cos(heading * Math.PI / 180); //y component of vector of ascent
    var xa = radiusA * Math.sin(heading * Math.PI / 180); //x component of vector of ascent

    var time = ascentRate * failure / descentRate;
    var radiusD = time * Dairspeed;
    var yd = radiusD * Math.cos(heading * Math.PI / 180); //y component of vector of descent
    var xd = radiusD * Math.sin(heading * Math.PI / 180); //x component of vector of descent

    //console.log(time+" "+ascentRate+" "+Dairspeed+" "+failure);

    var radiusW = 0;


    while (time > 0) {
        radiusW += math.eval(['t=' + time, equation])[1];
        time -= inc;
    }

    var yw = radiusW * Math.cos(Wheading * Math.PI / 180); //y component of vector of wind
    var xw = radiusW * Math.sin(Wheading * Math.PI / 180); //x component of vector of wind

    var ysum = ya + yd + yw;
    var xsum = xa + xd + xw;

    var searchTheta = -180 / Math.PI * Math.atan2(ysum, xsum);
    searchTheta = ((searchTheta < 0 ? searchTheta + 360 : searchTheta) + 90) % 360;
    var searchRadius = Math.sqrt(xsum ** 2 + ysum ** 2);

    /*
    console.log(xa)
    console.log(ya)

    console.log(xd)
    console.log(yd)

    console.log(xw)
    console.log(yw)

    console.log(xsum)
    console.log(ysum)

    console.log(searchTheta)
    console.log(searchRadius)

    console.log(radiusW)
    */

    console.log(JSON.stringify({ mag: searchRadius, angle: searchTheta }));
} catch (e) {
    console.error(e);
}

var spawn = require('child_process').spawn;

var child = spawn("node", ["./frontend/src/components/CalculateCrashZone/crashcalculator.1.js", JSON.stringify({ "heading": 184, "Aairspeed": 93, "ascent": 10, "failure": 43, "Dairspeed": 64, "descentRate": 6, "Wheading": 270, "equation": '-(1/720)*t^2+25' })]);

child.stdout.on('data', (data) => {
    data = data.toString();
    try {
        console.log(JSON.parse(data));
    } catch (e) {
        console.log(data);
    }

});
child.stderr.on('data', (data) => {
    console.log("Error:")
    console.log(data.toString());
});

/* Proof of concept:
console.log(180 / Math.PI * Math.atan2(3, -4))
console.log(180 / Math.PI * Math.atan2(3, 4))

console.log(180 / Math.PI * Math.atan2(-3, -4))
console.log(180 / Math.PI * Math.atan2(-3, 4))
*/
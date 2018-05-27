import React, { Component } from 'react';
import styles from "./CalculateCrashZone.css";
const math = require('mathjs');


export default class CrashZone extends Component {

    constructor(props) {
        super(props);
    }

    calcCrash() {
        var heading = 184;
        var Aairspeed = 93;
        var ascent = 10;
        var failure = 43;
        var Dairspeed = 64;
        var descentRate = 6;
        var Wheading = 270 - 180;


        var radiusA = Aairspeed * failure;
        var ya = radiusA * Math.cos(heading * Math.PI / 180); //y component of vector of ascent
        var xa = radiusA * Math.sin(heading * Math.PI / 180); //x component of vector of ascent

        var time = ascent * failure / descentRate;
        var radiusD = time * Dairspeed;
        var yd = radiusD * Math.cos(heading * Math.PI / 180); //y component of vector of descent
        var xd = radiusD * Math.sin(heading * Math.PI / 180); //x component of vector of descent

        var radiusW = 0;
        var inc = 0.01;

        var equation = "(-1/720 * x^2 + 25) * "+inc;

        var b = function() {
            var yw = radiusW * Math.cos(Wheading * Math.PI / 180); //y component of vector of wind
            var xw = radiusW * Math.sin(Wheading * Math.PI / 180); //x component of vector of wind

            var ysum = ya + yd + yw;
            var xsum = xa + xd + xw;

            var searchTheta = 180 / Math.PI * Math.atan(ysum / xsum);
            var searchRadius = Math.sqrt(xsum**2 + ysum**2);

            /*
            console.log(xa)
            console.log(ya)

            console.log(xd)
            console.log(yd)

            console.log(xw)
            console.log(yw)

            console.log(searchTheta)
            console.log(searchRadius)
            */

            console.log(radiusW);
            console.log($("."+styles.crashzone).val())
        }
        var a = function() {
            radiusW += math.eval(['x='+time, equation])[1];
            time -= inc;
            if (time > 0) {
                setTimeout(a, 0.0000000001);
            } else {
                console.log(time)
                b()
            }
        }

        setTimeout(a, 0.0000000001);
    }

    render() {
        return (
        <div className={styles.container}>
            <input className={styles.crashzone} />
            <button onClick={this.calcCrash} />
        </div>
        );
    }
}

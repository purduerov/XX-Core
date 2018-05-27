import React, { Component } from 'react';
import styles from "./CalculateCrashZone.css";


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
        var inc = 0.001
        while ( time > 0 ) {
            radiusW += (-(1.0/720) * time**2 + 25) * inc;
            time -= inc;
        }
        var yw = radiusW * Math.cos(Wheading * Math.PI / 180); //y component of vector of wind
        var xw = radiusW * Math.sin(Wheading * Math.PI / 180); //x component of vector of wind

        var ysum = ya + yd + yw;
        var xsum = xa + xd + xw;

        var searchTheta = Math.atan(ysum / xsum);
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

        console.log($("."+styles.crashzone).val())
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
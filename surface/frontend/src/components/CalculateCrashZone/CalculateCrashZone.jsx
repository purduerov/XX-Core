import React, { Component } from 'react';
import styles from "./CalculateCrashZone.css";
const math = require('mathjs');
const { ipcRenderer } = window.require('electron');


export default class CrashZone extends Component {

    constructor(props) {
        super(props);

        this.state = {calc: true};

        this.calcCrash = this.calcCrash.bind(this);
        this.resetCalc = this.resetCalc.bind(this);
    }

    calcCrash() {
        var btn = $("#planeCalcStart>button");
        if(btn.text() != "Please wait...") {
            btn.text("Please wait...");
            var planeParams = {}

            planeParams.startPoint = $("#planeStartPoint").val();
            planeParams.heading = Number($("#planeTakeoffHead").val());
            planeParams.Aairspeed = Number($("#planeAscSpeed").val());
            planeParams.ascentRate = Number($("#planeAscRate").val());
            planeParams.failure = Number($("#timeOfFailure").val());
            planeParams.Dairspeed = Number($("#planeDescSpeed").val());
            planeParams.descentRate = Number($("#planeDescRate").val());
            planeParams.Wheading = Number($("#windDirection").val());
            planeParams.equation = $("#windEquation").val();

            ipcRenderer.send('calc-crash', planeParams);

            ipcRenderer.on('crash-found', (event, data) => {
                console.log(data);
                if(data == 'error') {
                    alert("Invalid parameters likely to the crash calculating process, please try again");
                } else {

                    this.setState({
                        calc: false
                    }, () => {
                        $("#planeResults").text("The plane is roughly "+data.mag.toFixed(3)+" meters and "+data.angle.toFixed(3)+" degrees from "+planeParams.startPoint);
                    });
                }
            });
        }
    }

    resetCalc() {
        this.setState({
            calc: true
        }, () => {
            $("#planeCalcStart>button").text("Calculate landing zone");
        });
    }

    render() {
        return (
        <div className={styles.container}>
            {this.state.calc && <div id="planeCalcStart">
                <p>Wind speed equation (use t):</p>
                <input id="windEquation" defaultValue="-(1/720)*t^2+25" width="100%"/>
                <div className={styles.innerRow}>
                    <div className={styles.halfLeft} >
                        <p>Origin Location</p>
                        <input id="planeStartPoint" defaultValue="Naval Air Station Sand Point"/>
                        <p>Takeoff heading:</p>
                        <input id="planeTakeoffHead" defaultValue="184" />
                        <p>Ascent airspeed:</p>
                        <input id="planeAscSpeed" defaultValue="93" />
                        <p>Ascent rate:</p>
                        <input id="planeAscRate" defaultValue="10" />

                    </div>
                    <div className={styles.halfRight} >
                        <p>Time of Failure (sec):</p>
                        <input id="timeOfFailure" defaultValue="43"/>
                        <p>Descent airspeed:</p>
                        <input id="planeDescSpeed" defaultValue="64" />
                        <p>Descent rate:</p>
                        <input id="planeDescRate" defaultValue="6" />
                        <p>Wind blowing from:</p>
                        <input id="windDirection" defaultValue="270" />

                    </div>
                </div>
                <button onClick={this.calcCrash} >Calculate landing zone</button>
            </div>}
            {!this.state.calc && <div id="planeResultsContainer">
                <p id="planeResults" />
                <button onClick={this.resetCalc}>Reset Calculation</button>
            </div>}
        </div>
        );
    }
}

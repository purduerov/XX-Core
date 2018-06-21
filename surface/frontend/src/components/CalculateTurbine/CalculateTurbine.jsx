import React, {Component} from 'react';
import styles from "./CalculateTurbine.css";
const { ipcRenderer } = window.require('electron');

export default class Turbine extends Component {

  constructor(props) {
    super(props);

    this.state = {calc: true};
    this.calcTurb = this.calcTurb.bind(this);
    this.resetTurbine = this.resetTurbine.bind(this);
  }

  calcTurb() {
    var btn = $("#turbineCalcStart>button");
    if(btn.text() != "Please wait...") {
      btn.text("Please wait...");

      var count = Number($("#turbineCount").val());
      var diameter = Number($("#turbineDiameter").val());
      var velocity = Number($("#waterVelocity").val() * 0.514444);
      var efficiency = Number($("#turbineEfficiency").val());

      var area = 3.14159 * ((diameter / 2) ** 2);
      var power = count * .5 * 1025 * area * (velocity ** 3) * efficiency;

      this.setState({
        calc:false
      }, () => {
        $("#turbineResults").text("Power: " + power + " Watts");
      });
    }
  }

  resetTurbine() {
    this.setState({
      calc: true
    }, () => {
      $("turbineCalcStart>button").text("Calculate turbine power");
    });
  }

  render() {
    return(
      <div className={styles.container}>
        {this.state.calc && <div id="turbineCalcStart">
        <div className={styles.halfLeft} >
          <p>Quantity of turbines</p>
          <input id="turbineCount" defaultValue="1" />
          <p>Diameter of Turbine</p>
          <input id="turbineDiameter" defaultValue="2" />
        </div>
        <div className={styles.halfRight} >
          <p>Water Velocity</p>
          <input id="waterVelocity" defaultValue="3" />
          <p>Efficiency of Turbines</p>
          <input id="turbineEfficiency" defaultValue="4" />
        </div>
        <button id="turbineCalcStart" onClick={this.calcTurb} >Calculate turbine power</button>
      </div>}
      {!this.state.calc && <div id="turbineResultsContainer">
        <p id="turbineResults" />
        <button onClick={this.resetTurbine}>Reset Calculations</button>
    </div>}
    </div>
    );
  } //render
} //end export

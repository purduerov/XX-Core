import React, { Component } from 'react';
import styles from "./Seismograph.css";
import SeismographGraph from "./SeismographGraph.jsx";

//import './GoogleChartLibrary.js';

//google.charts.load('current', {'packages':['corechart']});
//google.charts.setOnLoadCallback(drawChart);

export default class Seismograph extends Component {

    constructor(props) {
        super(props);

        this.state = {graph: false, points: []};

        //this.state = {time: props.time, amp: props.amplitude};
        //console.log(props.time+", "+props.amplitude)

        this.disableRend = this.disableRend.bind(this);
        this.rendTime = this.rendTime.bind(this);
        this.rendAmp = this.rendAmp.bind(this);
        this.load = this.load.bind(this);
        this.componentDidMount = this.componentDidMount.bind(this);
        this.chartStuff = this.chartStuff.bind(this);
    }

    rendTime() {
      return this.props.time.map((val, index) => {
        return (
          <div key={"time"+index}>
            <hr className={styles.squashed}></hr>
            <div className={styles.time}>{val}</div>
          </div>
        )
      });
    }

    chartStuff() {
      return (
        <div id="chart_div" style="width: 900px; height: 500px;"></div>

      )
    }

    rendAmp() {
      return this.props.amplitude.map((val, index) => {
        return (
          <div key={"amp"+index}>
            <hr className={styles.squashed}></hr>
            <div className={styles.amplitude}>{val}</div>
          </div>
        )
      });
    }

    load() {
      var string = ($("#data").val());
      var pnts = [];
      string.split(", ").forEach((val, i) => {
        console.log(i+": "+parseFloat(val));
        pnts.push(parseFloat(val));
      });
      this.setState({
        points: pnts
      }, () => {
        //console.log(this.state);
      });
    }

    disableRend() {
      this.setState({
        graph: false
      });
    }

    componentDidMount() {
      $("."+styles.spawnButton).click(() => {
        this.setState({
          graph: true
        });
      });
    }

    render() {
        return (
        <div className={styles.container}>
          <div className={styles.halfRight}>
            <div>Times:</div>
            {this.rendTime()}
          </div>
          <div className={styles.halfLeft}>
            <div>Amplitudes:</div>
            {this.rendAmp()}
          </div>
          <div className={styles.bottom}>
            <input id="data" defaultValue="Insert comma Ordered List"></input>
            <button id="load" onClick={this.load} >Load Data</button>
          </div>
          {
            this.state.graph ?
            <SeismographGraph
              amplitude={this.state.points}
              rend={this.disableRend}
            ></SeismographGraph> : <p>"Press the button to generate a graph"</p>
          }
          <button className={styles.spawnButton}>Spawn Graph</button>
        </div>
        );
    }
}

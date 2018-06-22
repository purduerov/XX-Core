import React, { Component } from 'react';
import styles from "./SeismographGraph.css";
//import './GoogleChartLibrary.js';

//google.charts.load('current', {'packages':['corechart']});
//google.charts.setOnLoadCallback(drawChart);

export default class SeismographD3 extends Component {
  constructor(props) {
    super(props);

    //this.state = {time: props.time, amp: props.amplitude};

  }

  componentDidMount() {
    var graph = $("."+styles.fullMid);
    var points = []
    var i;

    //console.log(this.props.amplitude);
    for (i = 0; i < 16; i++) {
      points.push({x: (i + 1), y: this.props.amplitude[i]});
    }

    var options = {
      animationEnabled: true,
      title:{
        text: "Seismograph Data"
      },
      axisX: {
        title: "Time",
        includeZero: true
      },
      axisY: {
        title: "Amplitude",
        includeZero: true
      },
      data: [{
        yValueFormatString: "#,###.##",
        xValueFormatString: "#,###.##",
        type: "spline",
        dataPoints: points
      }]
    };
    graph.CanvasJSChart(options);

    $("."+styles.hideButton).click(this.props.rend);
  }

  render() {
    return (
    <div className={styles.container}>
      <div className={styles.fullMid}/>
      <button className={styles.hideButton} >Remove Graph</button>
    </div>
    );
  }
}

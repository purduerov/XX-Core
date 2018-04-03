import React, { Component } from 'react';
import styles from "./Seismograph.css";


export default class Seismograph extends Component {

    constructor(props) {
        super(props);

        //this.state = {time: props.time, amp: props.amplitude};
        console.log(props.time+", "+props.amplitude)

        this.rendTime = this.rendTime.bind(this);
        this.rendAmp = this.rendAmp.bind(this);
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
        </div>
        );
    }
}

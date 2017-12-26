import React, { Component } from 'react';
import Camera from 'react-camera';
import ThrusterCircle from './ThrusterCircle.jsx';
import styles from "./ThrusterInfo.css";


export default class ThrusterInfo extends Component {

  constructor(props) {
    super(props);
    
  }

  render() {
    return (
      <div className={styles.container}>
        <div className={styles.horizontal}>
          <ThrusterCircle className={styles.topLeft} val={Math.round(this.props.thrusters[0]*100)}/>
          <ThrusterCircle className={styles.topRight} val={Math.round(this.props.thrusters[1]*100)}/>
          <ThrusterCircle className={styles.bottomLeft} val={Math.round(this.props.thrusters[2]*100)}/>
          <ThrusterCircle className={styles.bottomRight} val={Math.round(this.props.thrusters[3]*100)}/>
        </div>
        <div className={styles.vertical}>
          <ThrusterCircle className={styles.topLeft} val={Math.round(this.props.thrusters[4]*100)}/>
          <ThrusterCircle className={styles.topRight} val={Math.round(this.props.thrusters[5]*100)}/>
          <ThrusterCircle className={styles.bottomLeft} val={Math.round(this.props.thrusters[6]*100)}/>
          <ThrusterCircle className={styles.bottomRight} val={Math.round(this.props.thrusters[7]*100)}/>
        </div>
      </div>
    );
  }
}
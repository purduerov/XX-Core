import React, { Component } from 'react';
import Camera from 'react-camera';
import ThrusterCircle from './ThrusterCircle.jsx';
import styles from "./ThrusterInfo.css";

/*

<ThrusterCircle className={styles.topLeft} val='5'/>
<ThrusterCircle className={styles.topRight} val='10'/>
<ThrusterCircle className={styles.bottomLeft} val='15'/>
<ThrusterCircle className={styles.bottomRight} val='20'/>


<ThrusterCircle className={styles.topLeft} val='40'/>
<ThrusterCircle className={styles.topRight} val='60'/>
<ThrusterCircle className={styles.bottomLeft} val='70'/>
<ThrusterCircle className={styles.bottomRight} val='80'/>

*/


export default class ThrusterInfo extends Component {

  constructor(props) {
    super(props);
    
  }

  render() {
    return (
      <div className={styles.container}>
        <div className={styles.horizontal}>
          <ThrusterCircle className={styles.topLeft} val='5'/>
          <ThrusterCircle className={styles.topRight} val='10'/>
          <ThrusterCircle className={styles.bottomLeft} val='15'/>
          <ThrusterCircle className={styles.bottomRight} val='20'/>
        </div>
        <div className={styles.vertical}>
          <ThrusterCircle className={styles.topLeft} val='40'/>
          <ThrusterCircle className={styles.topRight} val='60'/>
          <ThrusterCircle className={styles.bottomLeft} val='70'/>
          <ThrusterCircle className={styles.bottomRight} val='80'/>
        </div>
      </div>
    );
  }
}
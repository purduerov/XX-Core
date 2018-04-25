import React, { Component } from 'react';
import styles from "./ESCinfo.css";


export default class ESCinfo extends Component {

    constructor(props) {
        super(props);

        this.rendCur = this.rendCur.bind(this);
        this.rendTemp = this.rendTemp.bind(this);
        this.showESCcount = this.showESCcount.bind(this);
    }

    showESCcount() {
      return this.props.currents.map((val, index) => {
        return (
          <div key={"esc"+index}>
            <hr className={styles.squashed}></hr>
            <div className={styles.time}>{index+1}</div>
          </div>
        )
      });
    }

    rendCur() {
      return this.props.currents.map((val, index) => {
        return (
          <div key={"cur"+index}>
            <hr className={styles.squashed}></hr>
            <div className={styles.currents}>{val}</div>
          </div>
        )
      });
    }

    rendTemp() {
      return this.props.temp.map((val, index) => {
        return (
          <div key={"temp"+index}>
            <hr className={styles.squashed}></hr>
            <div className={styles.amplitude}>{val}</div>
          </div>
        )
      });
    }

    render() {
        return (
        <div className={styles.container}>
          <div className={styles.numCount}>
            <div>ESCs:</div>
            {this.showESCcount()}
          </div>
          <div className={styles.infoShow}>
            <div className={styles.halfRight}>
              <div>Current:</div>
              {this.rendCur()}
            </div>
            <div className={styles.halfLeft}>
              <div>Temp:</div>
              {this.rendTemp()}
            </div>
          </div>
        </div>
        );
    }
}

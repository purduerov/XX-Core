import React, { Component } from 'react';
import styles from "./CVview.css";


export default class CVview extends Component {

    constructor(props) {
        super(props);
    }

    getTailClassify() {
        var description;
        if(this.props.desc) {
          description = this.props.desc;
        } else {
          description = "";     //this will get replaced with the method to actually get the CV response, if the CV process is active
        }

        if(description) {
          return (
            <div>
              <div>
                Tail Classification:
              </div>
              <p className={styles.offLeft}>{description}</p>
            </div>
          )
        } else {
          return (
            <div>
              <p className={styles.offLeft}>Tail currently unclassified</p>
            </div>
          )
        }
    }

    getTurbineDistance() {
      var dist;
      if(this.props.tdist) {
        dist = this.props.tdist;
      } else {
        dist = [];    //this will get replaced with the method to actually get the CV response, if the CV process is active
      }

      if(dist) {
        return (
          <div>
            <div>
              Turbine Distance:
            </div>
            <p className={styles.offLeft}>{dist.join(', ')}</p>
          </div>
        )
      } else {
        return (
          <div>
            <p className={styles.offLeft}>Turbine distance not guaged</p>
          </div>
        )
      }
    }

    getTail

    render() {
        return (
        <div className={styles.container}>
            {this.getTailClassify()}
            {this.getTurbineDistance()}
        </div>
        );
    }
}

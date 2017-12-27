import React, { Component } from 'react';
import Camera from 'react-camera';
import ThrusterCircle from './ThrusterCircle.jsx';
import styles from "./ThrusterInfo.css";


export default class ThrusterInfo extends Component {

  constructor(props) {
    super(props);
    this.state = {'disabled': null};
    this.state.disabled = props.disabled;
    this.rendDisabled = this.rendDisabled.bind(this);
    
  }

  rendDisabled(val, indx) {
    let discpy = this.state.disabled;
    discpy[indx] = val;
    this.setState({
      disabled: discpy
    });
    this.props.rend(this.state.disabled);
  }

  render() {
    return (
      <div className={styles.container}>
        <div className={styles.horizontal}>
          <ThrusterCircle className={styles.topLeft} indx={0} rend={this.rendDisabled} val={Math.round(this.props.thrusters[0]*100)} disable={this.state.disabled[0]}/>
          <ThrusterCircle className={styles.topRight} indx={1} rend={this.rendDisabled} val={Math.round(this.props.thrusters[1]*100)} disable={this.state.disabled[1]}/>
          <ThrusterCircle className={styles.bottomLeft} indx={2} rend={this.rendDisabled} val={Math.round(this.props.thrusters[2]*100)} disable={this.state.disabled[2]}/>
          <ThrusterCircle className={styles.bottomRight} indx={3} rend={this.rendDisabled} val={Math.round(this.props.thrusters[3]*100)} disable={this.state.disabled[3]}/>
        </div>
        <div className={styles.vertical}>
          <ThrusterCircle className={styles.topLeft} indx={4} rend={this.rendDisabled} val={Math.round(this.props.thrusters[4]*100)} disable={this.state.disabled[4]}/>
          <ThrusterCircle className={styles.topRight} indx={5} rend={this.rendDisabled} val={Math.round(this.props.thrusters[5]*100)} disable={this.state.disabled[5]}/>
          <ThrusterCircle className={styles.bottomLeft} indx={6} rend={this.rendDisabled} val={Math.round(this.props.thrusters[6]*100)} disable={this.state.disabled[6]}/>
          <ThrusterCircle className={styles.bottomRight} indx={7} rend={this.rendDisabled} val={Math.round(this.props.thrusters[7]*100)} disable={this.state.disabled[7]}/>
        </div>
      </div>
    );
  }
}
import React, { Component } from 'react';
import styles from "./Gpinfo.css";

export default class Gpinfo extends Component {
  constructor(props) {
    super(props);

    this.renderReady = this.renderReady.bind(this);
  }

  renderReady() {
    if(this.props.ready === true) {
      return ( <div>
          <div>
            <ul className={styles.ButtonNames}>
                <li>a: {this.props.buttons.a.curVal}</li>
                <li>b: {this.props.buttons.b.curVal}</li>
                <li>x: {this.props.buttons.x.curVal}</li>
                <li>y: {this.props.buttons.y.curVal}</li>
                <li>lb: {this.props.buttons.lb.curVal}</li>
                <li>rb: {this.props.buttons.rb.curVal}</li>
                <li>select: {this.props.buttons.select.curVal}</li>
                <li>start: {this.props.buttons.start.curVal}</li>
                <li>lpress: {this.props.buttons.lpress.curVal}</li>
                <li>rpress: {this.props.buttons.rpress.curVal}</li>
                <li>up: {this.props.buttons.up.curVal}</li>
                <li>down: {this.props.buttons.down.curVal}</li>
                <li>left: {this.props.buttons.left.curVal}</li>
                <li>right: {this.props.buttons.right.curVal}</li>
              </ul>
          </div>
          <div>
            <ul className={styles.AxisNames}>
            <li>LstickXaxis: {this.props.axes.LstickXaxis.curVal}</li>
            <li>LstickYaxis: {this.props.axes.LstickYaxis.curVal}</li>
            <li>RstickXaxis: {this.props.axes.RstickXaxis.curVal}</li>
            <li>RstickYaxis: {this.props.axes.RstickYaxis.curVal}</li>
            <li>Ltrigger: {this.props.axes.Ltrigger.curVal}</li>
            <li>Rtrigger: {this.props.axes.Rtrigger.curVal}</li>
            </ul>
          </div>
          <div>
            <ul>
            <li>upchk: {this.props.up}</li>
            <li>dwnchk: {this.props.down}</li>
            </ul>
          </div>
        </div>
      )
    } else {
      return (
        <div className={styles.NOTREADY}>"GP is not mapped"</div>
      )
    }
  }

  render() {
      return (
      <div container={styles.container}>
          <h1>Gamepad</h1>
          <hr />
          <div className={styles.Gamepad}>
            {this.renderReady()}
          </div>
      </div>
      );
  }
}

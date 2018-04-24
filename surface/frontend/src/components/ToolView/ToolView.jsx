import React, { Component } from 'react';
import {render} from 'react-dom';
import styles from './ToolView.css';

export default class ToolView extends Component {
  constructor(props) {
    super(props);

    this.state = {conf: props.conf};

    this.rendTool = this.rendTool.bind(this);
    this.onChangeCheck = this.onChangeCheck.bind(this);
  }

  onChangeCheck(e) {
      let confcpy = this.state.conf;
      //console.log(e.target.id)
      confcpy[e.target.id].invert = (e.target.checked-0.5)*-2;
      this.props.rend(confcpy);
      /*this.setState({conf: confcpy}, function() {
          this.props.rend(this.state.val, this.state.inv, this.props.indx);
          //console.log(this.state.inv);
      });*/
  }

  rendTool() {
    var axis = ['manipulator', 'obs_tool', 'servo', 'transmitter', 'magnet'];
    return axis.map((val, index) => {
      return (
        <li key={'axis'+val} >
          <p className={styles.lowMargin}>{val}: {typeof this.props[val] == "boolean" ? (this.props[val]?1:0) : this.props[val].toFixed(2)}
          {this.state.conf[val] != undefined &&
          <span className={styles.right}>
              <input type="checkbox" id={val} defaultChecked={this.props.conf[val].invert===-1} onClick={this.onChangeCheck} />
              <label>Invert</label>
          </span>}
          </p>
        </li>
      );
    });

  }

  render() {
      return (
        <div className={styles.container}>
          <div className={styles.ToolView}>
            <ul>
              {this.rendTool()}
            </ul>
          </div>
        </div>
      )
  }

} //end export

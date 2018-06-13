import React, { Component } from 'react';
import {render} from 'react-dom';
import SliderControl from '../SliderControl/SliderControl.jsx';
import styles from './ToolView.css';

export default class ToolView extends Component {
  constructor(props) {
    super(props);

    this.state = {conf: props.conf};
    this.axis = ['manipulator', 'obs_tool', 'servo', 'transmitter', 'magnet'];

    this.rendTool = this.rendTool.bind(this);
    this.reRender = this.reRender.bind(this);
  }

  reRender(val, inv, tool) {
      let confcpy = this.state.conf;
      //console.log(e.target.id)
      confcpy[tool].invert = inv;
      confcpy[tool].master = val / 100;
      this.props.rend(confcpy);
      /*this.setState({conf: confcpy}, function() {
          this.props.rend(this.state.val, this.state.inv, this.props.indx);
          //console.log(this.state.inv);
      });*/
  }

  rendTool() {
    return this.axis.map((val, index) => {
      return (
        <li key={'axis'+val} >
        {this.state.conf[val] == undefined &&<p className={styles.lowMargin}>{val}: {typeof this.props[val] == "boolean" ? (this.props[val]?1:0) : this.props[val].toFixed(2)}</p>}
        {this.state.conf[val] != undefined &&
          <SliderControl min='0' max='50' key={val} indx={val} power={this.state.conf[val].master*100} invert={this.state.conf[val].invert} rend={this.reRender} name={val} />}
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

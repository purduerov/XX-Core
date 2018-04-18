import React, { Component } from 'react';
import {render} from 'react-dom';
import styles from './ToolView.css';

export default class ToolView extends Component {
  constructor(props) {
    super(props);

    this.rendTool = this.rendTool.bind(this);
  }

  rendTool() {
    var axis = ['manipulator', 'obstool'];
    return axis.map((val, index) => {
      return (
        <li key={'axis'+val} >
          {val}: {this.props[val]}
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

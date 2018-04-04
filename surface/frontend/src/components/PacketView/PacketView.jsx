import React, { Component } from 'react';
import {render} from 'react-dom';
import styles from './PacketView.css';

export default class PacketView extends Component {
  constructor(props) {
    super(props);

    this.rendPacket = this.rendPacket.bind(this);
  }

  rendPacket() {
    var axis = ['x', 'y', 'z', 'roll', 'pitch', 'yaw'];
    return axis.map((val, index) => {
      return (
        <li key={'axis'+val} >
          {axis[index]}: {this.props.packet[index]}
        </li>
      );
    });
  }

  render() {
      return (
        <div className={styles.container}>
          <div className={styles.PacketView}>
            <ul>
              {this.rendPacket()}
            </ul>
          </div>
        </div>
      )
  }

} //end export

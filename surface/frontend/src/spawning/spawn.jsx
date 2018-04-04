import React, { Component } from 'react';
import {render} from 'react-dom';
import styles from "./spawn.css";
const fs = window.require('fs');
const { ipcRenderer } = window.require('electron');

export default class Spawn extends Component {
  constructor(props) {
    super(props);

    this.RendButton = this.RendButton.bind(this);
  }

  RendButton() {
    return (
      <button
        className={styles.btn}
        onClick={this.handleClick}>
        Spawn CV
      </button>
    )
  }

  render() {
    return (
      <div container={styles.container}>
        <div className={styles.butn}>
          {this.RendButton()}
        </div>
      </div>
    );
  }

  handleClick() {
  console.log('success!')

     ipcRenderer.send('spawn-event', 'werk bitch')
     
     ipcRenderer.on('spawn-reply', (event,arg) => {
       console.log(arg)
     })
   } //end handleClick



   // ipcRenderer.on('spawn-receive', (event, arg) => {
   //   console.log(arg)

   //})


} //end export

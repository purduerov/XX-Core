import React, { Component } from 'react';
import {render} from 'react-dom';
import styles from "./spawn.css";
const fs = window.require('fs');
const { ipcRenderer } = window.require('electron');

export default class Spawn extends Component {
  constructor(props) {
    super(props);

    this.state = {
      filenames: {}
    };

    ipcRenderer.send('find-files');

    ipcRenderer.on('files-found', (event, args) => {
      console.log(args);
      this.filenames = args;
      this.setState({filenames: this.filenames});
    });

    ipcRenderer.on("cv-spawned", (event, file) => {
      this.filenames[file.name].on = file.on;
      console.log(file.extra);
      console.log(this.filenames)

      this.setState({filenames: this.filenames});
    });

    this.rendButtons = this.rendButtons.bind(this);
  }

  interactCV(val) {
    console.log(val);

    ipcRenderer.send('cv-spawn', val);
  }

  rendButtons() {
    return Object.keys(this.state.filenames).map((val, index) => {
      return (
        <div className={styles.cvpod} key={val}>
          <p>{val}</p>
          <button val={val} onClick={() => this.interactCV(val)} >{"turn "+(!this.state.filenames[val].on?"on":"off")}</button>
        </div>
      )
    });
  }

  render() {
    return (
      <div container={styles.container}>
        {this.rendButtons()}
      </div>
    );
  }

  handleClick() {
    ipcRenderer.send('spawn-event', 'Spawning 2.0.2, Electric Confugaloo');

    ipcRenderer.on('spawn-reply', (event,arg) => {
       console.log(arg);
    });
 } //end handleClick



   // ipcRenderer.on('spawn-receive', (event, arg) => {
   //   console.log(arg)

   //})


} //end export

import React, { Component } from 'react';
import Camera from 'react-camera';
import styles from './Cam_View.css'


export default class Camera_view extends Component {

  constructor(props) {
    super(props);
    this.takePicture = this.takePicture.bind(this);
    this.state = {
      pxybypass: false,
      camscreen1: 0,
      camscreen2: 1,
      camnames: [
                "Cam1",
                "Cam2",
                "Cam3",
                "Cam4",
                "Cam5"
                ]
    }
  }

  takePicture() {
    this.camera.capture()
    .then(blob => {
      this.img.src = URL.createObjectURL(blob);
      this.img.onload = () => { URL.revokeObjectURL(this.src); }
    })
  }

  render() {
    return (
      <div className={styles.container}>
      <img src="http://localhost:1917/?action=stream_0"></img>
      </div>
    );
  }
}

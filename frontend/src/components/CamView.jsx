import React, { Component } from 'react';
import Camera from 'react-camera';
import styles from './Cam_View.css'


export default class Camera_view extends Component {

  constructor(props) {
    super(props);
    this.takePicture = this.takePicture.bind(this);
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
        <Camera
          className={styles.preview}
          ref={(cam) => {
            this.camera = cam;
          }}
        >
        </Camera>
        <img
          className={styles.captureImage}
          ref={(img) => {
            this.img = img;
          }}
        />
      </div>
    );
  }
}

import React, { Component } from 'react';
import Camera from 'react-camera';
import styles from './Cam_View.css'

class CamSel extends React.Component {
    render() {
          return (
                  <button className="camsel" onClick={()=>{}}>
                  </button>
                  );
        }
}

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
        <header>CAMERA1 CAMERA2</header>
        <div className ={styles.contentBox} >

          <div className={styles.column1} >
           CONTENT
          </div>

          <div className={styles.column2} >
              <img src="http://localhost:1917/?action=stream" height="350"></img>
          </div>

        </div>

      </div>
    );
  }
}

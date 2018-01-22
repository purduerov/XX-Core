import React, { Component } from 'react';
import Camera from 'react-camera';
import styles from './Cam_View.css'

class Square extends React.Component {
  render() {
    return (
      <div> <button className={styles.butt} onClick={()=>this.props.onClick()}>
        {this.props.value}
      </button></div>
     );
  }
}

class CamSel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      sub:"Name"
    };
    this.handleNameChange = this.handleNameChange.bind(this);
    this.handleSubmitChange = this.handleSubmitChange.bind(this);
  }

  handleNameChange(event) {
    this.setState({ name: event.target.value });
  };
  handleSubmitChange(event){
    this.props.onUpdate(event.target.value)
  }

  render() {
    return (
      <div>
        <input
          type="text"
          value={this.state.name}
          onChange={this.handleNameChange}
        />
        <input
          type="submit"
          value={this.state.sub}
          onChange={this.handleSubmitChange}
        />
      </div>
    );
  }
}


export default class Camera_view extends Component {

  constructor(props) {
    super(props);
    this.takePicture = this.takePicture.bind(this);
    this.state = {
      pxybypass: false,
      camscreens: [
                  0,
                  1
                  ],
      camnames: [
                "Cam1",
                "Cam2",
                "Cam3",
                "Cam4",
                "Cam5"
                ],
      CVprocsNames: ["ProcName1","ProcName2"],
      CVprocsPorts: [1917,1918],
      CVprocsActiv: [false,false]
    }
  }

  takePicture() {
    this.camera.capture()
    .then(blob => {
      this.img.src = URL.createObjectURL(blob);
      this.img.onload = () => { URL.revokeObjectURL(this.src); }
    })
  }

  handleClick(screennum,camnum){
    const camscreens = this.state.camscreens.slice();
    camscreens[screennum] = camnum;
    this.setState({
      camscreens: camscreens
    })


  }

  renderSquare(screennum,camnum) {
    return <Square value={this.state.camnames[camnum]} 
      onClick={() => this.handleClick(screennum, camnum)}/>;
  }

  camUpdate(newName){
        const camnames = this.state.camnames.slice();
        camnames[1] = newName;
        this.setState({
          camnames: camnames
        })
  }
  renderCamSel(screennum) {
    return <CamSel onUpdate={()=>this.camUpdate("Blah")}/>;
  }

  render() {
    return (
      <div className={styles.container}>
        <header className={styles.header}>
          <div>Screen1:  {this.renderCamSel(0)}</div> 
          <div>Screen2:  {this.renderCamSel(1)}</div>
        </header>
        <div className ={styles.contentBox} >
          <div className={styles.column1} >
           {this.renderSquare(0, 0)}
           {this.renderSquare(0, 1)}
           {this.renderSquare(0, 2)}
           {this.renderSquare(0, 3)}
           {this.renderSquare(0, 4)}
          </div>
          <div className={styles.column2} >
              <img src="http://localhost:1917/?action=stream_0" height="350"></img>
          </div>
        </div>
        <div className ={styles.contentBox} >
          <div className={styles.column1} >
           {this.renderSquare(1, 0)}
           {this.renderSquare(1, 1)}
           {this.renderSquare(1, 2)}
           {this.renderSquare(1, 3)}
           {this.renderSquare(1, 4)}
          </div>
          <div className={styles.column2} >
            <img src="http://localhost:1917/?action=stream_0" height="350"></img>
          </div>
        </div>
      </div>
    );
  }
}

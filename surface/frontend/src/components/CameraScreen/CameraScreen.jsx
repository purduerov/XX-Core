import React, {Component} from 'react';
import Camera from 'react-camera';
import styles from './CameraScreen.css'

class Square extends React.Component {
    render() {
        return (
              <button className={styles.butt} onClick={() => this.props.onClick()}>
                  {this.props.value}
              </button>
        );
    }
}

class Stream extends React.Component {
    render() {
        return (
            <img src={this.props.cam} width="100%"></img>
        )
    }
}

class CamSel extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: '',
            sub: "Name"
        };
        this.handleNameChange = this.handleNameChange.bind(this)
    }

    handleNameChange(event) {
        this.setState({name: event.target.value})
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
                    onClick={(e) => this.props.onNewName(this.state.name)}
                />
            </div>
        );
    }
}

function getMoviesFromApiAsync(callback) {
           return fetch('http://localhost:1905')
           .then((response) => response.json())
           .then((results)=>{
                callback(results);
            });
    }
export default class Camera_view extends Component {

    constructor(props) {
        super(props);

        this.state = {
            pxybypass: true,
            pakconf:{},
            numcams:1, //Change to the number of accessable cams. For future growth use pakfornt api
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
            stream : {
                ip: "localhost",
                query: "/?action=stream_",
                rovip:"raspberrypi.local"
            },
            camnext: props.next,
            camprev: props.prev,
            prevcamnext: 0,
            prevcamprev: 0
        }
        this.getconf()
    }

    getconf(){
           if(!this.state.pxybypass){
                   return fetch('http://localhost:1905')
                   .then((response) => response.json())
                   .then((results)=>{
                        this.setState({
                            pakconf: results
                        })
                    });
        }
    }
    handleClick(screennum, camnum) {
        const camscreens = this.state.camscreens.slice();
        camscreens[screennum] = camnum;
        this.setState({
            camscreens: camscreens
        })


    }

    camUpdate(screennum, newName) {
        const camnames = this.state.camnames.slice();
        camnames[this.state.camscreens[screennum]] = newName;
        this.setState({
            camnames: camnames
        })
    }
    checkPrevPress(){
        if (this.state.camnext === 1 && this.state.prevcamnext=== 0){
                return true
        }
        this.state.prevcamnext = this.state.camnext;
        return false
    }
    checkNextPress(){
        if (this.state.camprev === 1 && this.state.prevcamprev=== 0){
                return true
        }
        this.state.prevcamprev = this.state.camprev;
        return false
    }
    renderCamSel(screennum) {
        return <CamSel onNewName={(val) => this.camUpdate(screennum,val)}/>;
    }

    renderStream(strnum) {
        if(this.checkPrevPress()){
                const camscreens = this.state.camscreens.slice();
                camscreens[strnum] = camscreens[strnum]-1;
                if(camscreens[strnum] === -1){
                        camscreens[strnum] = this.state.numcams;
                }
                this.setState({
                    camscreens: camscreens
                })
        }
        if(this.checkNextPress()){
                const camscreens = this.state.camscreens.slice();
                camscreens[strnum] = (camscreens[strnum]+1)%this.state.numcams;
                this.setState({
                    camscreens: camscreens
                })

        }
        var camnum = this.state.camscreens[strnum];
        if(camnum >= this.state.numcams){
                camnum = 0;
        }
        let port;
        let query = '';
        if(typeof this.state.pakconf.socketio !== 'undefined'){
        switch(camnum) {
                case 0:
                        port = this.state.pakconf.camnum0.stream;
                break;
                case 1:
                        port = this.state.pakconf.camnum1.stream;
                break;
                case 2:
                        port = this.state.pakconf.camnum2.stream;
                break;
                case 3:
                        port = this.state.pakconf.camnum3.stream;
                break;
                case 4:
                        port = this.state.pakconf.camnum4.stream;
                break;
                default:
                        port = this.state.pakconf.camnum0.stream;
        }
        }else{
                port = 8000
        }
	var IP
        if(this.state.pxybypass){
                port = 8080;
                query = this.state.stream.query + this.state.camscreens[strnum];
		IP = this.state.stream.rovip
        }else{
		IP = this.state.stream.ip
	}
        let url = "http://" + IP + ":" + port + query;
        return <Stream cam={url}/>
    }

    renderSquare(screennum, camnum) {
        return <Square value={this.state.camnames[camnum]}
                       onClick={() => this.handleClick(screennum, camnum)}/>;
    }

    render() {
        return (
            <div className={styles.container}>
                <header className={styles.header}>
                    <div className={styles.whiteText}>Screen1: {this.renderCamSel(0)}</div>
                </header>
                <div className={styles.contentBox}>
                    <div className={styles.column2}>
                        {this.renderStream(0)}
                    </div>
                        <div className={styles.column1}>
                            {this.renderSquare(0, 0)}
                            {this.renderSquare(0, 1)}
                            {this.renderSquare(0, 2)}
                            {this.renderSquare(0, 3)}
                            {this.renderSquare(0, 4)}
                        </div>
                </div>
            </div>
        );
    }
}

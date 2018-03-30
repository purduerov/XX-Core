import React, {Component} from 'react';
import Camera from 'react-camera';
import styles from './Cam_View.css'

class Square extends React.Component {
    render() {
        return (
            <div>
                <button className={styles.butt} onClick={() => this.props.onClick()}>
                    {this.props.value}
                </button>
            </div>
        );
    }
}

class Stream extends React.Component {
    render() {
        return (
            <img src={this.props.cam} height="350"></img>
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


export default class Camera_view extends Component {

    constructor(props) {
        super(props);
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
            stream : {
                ip: "localhost",
                query: "",
                rovip:"raspberrypi.local",
                startport:8080
            }
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

    renderCamSel(screennum) {
        return <CamSel onNewName={(val) => this.camUpdate(screennum,val)}/>;
    }

    renderStream(strnum) {
        let url = "http://" + this.state.stream.ip + ":" + (this.state.stream.startport + this.state.camscreens[strnum]);
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
                    <div>Screen1: {this.renderCamSel(0)}</div>
                    <div>Screen2: {this.renderCamSel(1)}</div>
                </header>
                <div className={styles.contentBox}>
                    <div className={styles.column1}>
                        {this.renderSquare(0, 0)}
                        {this.renderSquare(0, 1)}
                        {this.renderSquare(0, 2)}
                        {this.renderSquare(0, 3)}
                        {this.renderSquare(0, 4)}
                    </div>
                    <div className={styles.column2}>
                        {this.renderStream(0)}
                    </div>
                </div>
                <div className={styles.contentBox}>
                    <div className={styles.column1}>
                        {this.renderSquare(1, 0)}
                        {this.renderSquare(1, 1)}
                        {this.renderSquare(1, 2)}
                        {this.renderSquare(1, 3)}
                        {this.renderSquare(1, 4)}
                    </div>
                    <div className={styles.column2}>
                        {this.renderStream(1)}
                    </div>
                </div>
            </div>
        );
    }
}

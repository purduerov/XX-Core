import React, { Component } from 'react';
import Camera from 'react-camera';
import styles from "./SliderControl.css";


export default class SliderControl extends Component {

    constructor(props) {
        super(props);
        this.state = {'val': null, 'onoff': null};
        this.state.val = props.val;
        this.state.inv = props.inv;
        this.onChangeCheck = this.onChangeCheck.bind(this);
        this.onChangeVal = this.onChangeVal.bind(this);
    }

    onChangeCheck(e) {
        console.log(e.target.checked+" vs "+this.state.inv);
        let valcpy = this.state.val;
        this.setState({inv: (e.target.checked-0.5)*2, val: valcpy});
        this.props.rend(this.state.val, this.state.inv, this.props.indx);
    }

    onChangeVal(e) {
        console.log(e.target.value+" vs "+this.state.val);
        let invcpy = this.state.inv;
        this.setState({inv: invcpy, val: e.target.value});
        this.props.rend(this.state.val, this.state.inv);
    }

    render() {
        return (
        <div className={styles.container}> 
            <div>
                <span>{this.props.name}: {this.state.val}%</span>
                {this.props.inv != undefined &&
                <span className={styles.right}>
                    <input type="checkbox" defaultChecked={this.state.inv===-1} onClick={this.onChangeCheck} />
                    <label>Invert</label>
                </span>}
            </div>
            <input className="hugtop" type="range" min={this.props.min} max={this.props.max} value={this.state.val} onChange={this.onChangeVal} />
        </div>
        );
    }
}

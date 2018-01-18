import React, { Component } from 'react';
import Camera from 'react-camera';
import styles from "./SliderControl.css";


export default class SliderControl extends Component {

    constructor(props) {
        super(props);
        this.state = {val: props.val.power, inv: props.val.invert};

        this.onChangeCheck = this.onChangeCheck.bind(this);
        this.onChangeVal = this.onChangeVal.bind(this);
    }

    onChangeCheck(e) {
        let valcpy = this.state.val;
        this.setState({inv: (e.target.checked-0.5)*-2, val: valcpy}, function() {
            this.props.rend(this.state.val, this.state.inv, this.props.indx);
            //console.log(this.state.inv);
        });
    }

    onChangeVal(e) {
        let invcpy = this.state.inv;
        this.setState({inv: invcpy, val: e.target.value}, function() {
            this.props.rend(this.state.val, this.state.inv, this.props.indx);
            //console.log(this.state.val);
        });
    }

    render() {
        return (
        <div className={styles.container}> 
            <div className={styles.killPad}>
                <p className={styles.fill}>{this.props.name}:</p>
                <p className={styles.left}>{this.state.val}%</p>
                {this.state.inv != undefined &&
                <p className={styles.right}>
                    <input type="checkbox" defaultChecked={this.state.inv===-1} onClick={this.onChangeCheck} />
                    <label>Invert</label>
                </p>}
            </div>
            <input className="hugtop" type="range" min={this.props.min} max={this.props.max} value={this.state.val} onChange={this.onChangeVal} />
        </div>
        );
    }
}

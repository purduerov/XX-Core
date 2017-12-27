import React, { Component } from 'react';
import Camera from 'react-camera';
import styles from "./SliderControl.css";


export default class SliderControl extends Component {

    constructor(props) {
        super(props);
        this.state = {'val': null, 'onoff': null};
        this.state.val = props.val;
        this.state.onoff = props.onoff;
    }

    rendScales(thrusts, rend) {
        return thrusts.scales.map(function(scale, index) {
            <SliderControl min='0' max='100' key={'thrust'+index} val={scale} 
                    onoff={thrusts.onoff} rend={rend} name={"Thruster "+(index+1)} />
        });
    }

    onChangeCheck(e) {
        let valcpy = this.state.val;
        this.setState({onoff: !e.target.checked, val: valcpy});
        this.props.rend(this.state.val, this.state.onoff);
    }

    onChangeVal(e) {
        let onoffcpy = this.state.onoff;
        this.setState({onoff: onoffcpy, val: e.target.value});
        this.props.rend(this.state.val, this.state.onoff);
    }

    render() {
        return (
        <div className={styles.container}> 
            <div>
                <span>{this.props.name}: {this.props.val}%</span>
                {this.props.onoff != undefined &&
                <span className={styles.right}>
                    <input type="checkbox" defaultChecked={!this.state.onoff} onClick={this.onChangeCheck.bind(this)} />
                    <label>Disable</label>
                </span>}
            </div>
            <input type="range" min={this.props.min} max={this.props.max} value={this.state.val} onChange={this.onChangeVal.bind(this)} />
        </div>
        );
    }
}

import React, { Component } from 'react';
import Camera from 'react-camera';
import SliderControl from './SliderControl.jsx';
//import styles from "./ThrusterScales.css";


export default class ThrusterScales extends Component {

    constructor(props) {
        super(props);
        this.state = {'scales': null, 'onoff': null};
        this.state.scales = props.scales;
        this.state.onoff = props.onoff;
        console.log(this.props);
        this.rendScales = this.rendScales.bind(this);
    }

    rendData(val, onoff, i) {
        this.state.scales[i] = val;
        this.state.onoff[i] = onoff;

        this.props.rend(this.state.scales, this.state.onoff);
    }

    rendScales() {
        let that = this;
        return this.state.scales.map(function(scale, index) {
            <SliderControl min='0' max='100' key={'thrust'+index} val={scale} onoff={that.state.onoff[index]} rend={that.rendData.bind(that)} name={"Thruster "+(index+1)} />
        });
    }

    render() {
        return (
            <div>
                <SliderControl min='0' max='100' key={'thrust0'} val={this.state.scales[0]} onoff={this.state.onoff[0]} rend={this.rendData.bind(this)} name={"Thruster 0"} />
                {this.rendScales()}
            </div>
        );
    }
}
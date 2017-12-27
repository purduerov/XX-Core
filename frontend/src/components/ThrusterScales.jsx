import React, { Component } from 'react';
import Camera from 'react-camera';
import SliderControl from './SliderControl.jsx';
//import styles from "./ThrusterScales.css";

let that;

/*
    <SliderControl min='0' max='100' key={'thrust0'} indx={0} val={this.state.scales[0]} inv={this.state.inv[0]} rend={this.rendData.bind(this)} name={"Thruster 0"} />
*/

export default class ThrusterScales extends Component {

    constructor(props) {
        super(props);
        this.state = {'scales': null, 'inv': null};
        this.state.scales = props.scales;
        this.state.inv = props.inv;
        console.log(this.props);
        this.rendScales = this.rendScales.bind(this);

        that = this;
    }

    rendData(val, inv, i) {
        this.state.scales[i] = val;
        this.state.inv[i] = inv;

        this.props.rend(this.state.scales, this.state.inv);
    }

    rendScales() {
        return that.state.scales.map(function(scale, index) {
                    console.log(index);
                    return (
                        <SliderControl min='0' max='100' key={'thrust'+index} indx={index} val={scale} inv={that.state.inv[index]} rend={that.rendData.bind(that)} name={"Thruster "+(index+1)} />
                    );
                });
    }

    render() {
        return (
            <div>
                {this.rendScales()}
            </div>
        );
    }
}
import React, { Component } from 'react';
import SliderControl from '../SliderControl/SliderControl.jsx';
import styles from "./ThrusterScales.css";

let that;

/*
    <SliderControl min='0' max='100' key={'thrust0'} indx={0} val={this.state.scales[0]} inv={this.state.inv[0]} rend={this.rendData.bind(this)} name={"Thruster 0"} />
*/

export default class ThrusterScales extends Component {

    constructor(props) {
        super(props);
        this.state = {'scales': props.scales};

        this.rendLeftScales = this.rendLeftScales.bind(this);
        this.rendRightScales = this.rendRightScales.bind(this);

        that = this;
    }

    rendData(val, inv, i) {
        //console.log(this.state.scales[i]);
        //console.log(this.state.scales[i].power);
        let scalescpy = this.state.scales;
        scalescpy[i].power = val;
        scalescpy[i].invert = inv;
        this.setState({
            scales: scalescpy
        }, function() {
            this.props.rend(this.state.scales);
        });
    }

    rendLeftScales() {
        return [0, 1, 2, 3].map(function(val, index) {
                    return (
                        <SliderControl min='0' max='100' key={'thrust'+val} indx={val} power={that.state.scales[val].power} inv={that.state.scales[val].invert} rend={that.rendData.bind(that)} name={"Thruster "+(val+1)} />
                    );
                });
    }

    rendRightScales() {
        return [4, 5, 6, 7].map(function(val, index) {
                    return (
                        <SliderControl min='0' max='100' key={'thrust'+val} indx={val} power={that.state.scales[val].power} inv={that.state.scales[val].invert} rend={that.rendData.bind(that)} name={"Thruster "+(val+1)} />
                    );
                });
    }

    render() {
        return (
            <div className={styles.container}>
                <div className={styles.halfLeft}>
                    {this.rendLeftScales()}
                </div>
                <div className={styles.halfRight}>
                    {this.rendRightScales()}
                </div>
            </div>
        );
    }
}

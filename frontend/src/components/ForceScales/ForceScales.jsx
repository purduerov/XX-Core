import React, { Component } from 'react';
import SliderControl from '../SliderControl/SliderControl.jsx';
import styles from "./ForceScales.css";

let that;

/*
    <SliderControl min='0' max='100' key={'thrust0'} indx={0} val={this.state.scales[0]} inv={this.state.inv[0]} rend={this.rendData.bind(this)} name={"Thruster 0"} />
*/

export default class ForceScale extends Component {

    constructor(props) {
        super(props);
        this.state = {'scales': props.scales};

        this.rendLeftScales = this.rendLeftScales.bind(this);
        this.rendRightScales = this.rendRightScales.bind(this);

        that = this;
    }

    rendData(val, inv, key) {
        //console.log(this.state.scales[key]);
        let scalescpy = this.state.scales;
        scalescpy[key] = val;
        //scalescpy[key].invert = inv;
        this.setState({
            scales: scalescpy
        }, function() {
            this.props.rend(this.state.scales);
        });
    }

    rendLeftScales() {
        return Object.keys(this.props.scales).map(function(val, index) {
            if(val.slice(0,3) === "vel")
            {
                return (
                    <SliderControl min='0' max='100' key={'force'+val} indx={val} power={that.state.scales[val]} rend={that.rendData.bind(that)} name={"Force "+(val.slice(-1))} />
                );
            }
        });
    }

    rendRightScales() {
        return Object.keys(this.props.scales).map(function(val, index) {
            if(val.slice(0,3) !== "vel" && val !== "master")
            {
                return (
                    <SliderControl min='0' max='100' key={'force'+val} indx={val} power={that.state.scales[val]} rend={that.rendData.bind(that)} name={"Force "+(val)} />
                );
            }
        });
    }

    render() {
        return (
            <div className={styles.container}>
                <div className={styles.fullAll} >
                    <SliderControl min='0' max='100' key={'force master'} indx={'master'} power={that.state.scales['master']} rend={that.rendData.bind(that)} name={"Force master"} />
                    <div className={styles.halfLeft}>
                        {this.rendLeftScales()}
                    </div>
                    <div className={styles.halfRight}>
                        {this.rendRightScales()}
                    </div>
                </div>
            </div>
        );
    }
}

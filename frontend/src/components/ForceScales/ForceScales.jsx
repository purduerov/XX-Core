import React, { Component } from 'react';
import SliderControl from '../SliderControl/SliderControl.jsx';
import styles from './ForceScales.css';

/*
    <SliderControl min='0' max='100' key={'thrust0'} indx={0} val={this.state.scales[0]} inv={this.state.inv[0]} rend={this.rendData.bind(this)} name={"Thruster 0"} />
*/

export default class ForceScale extends Component {
    constructor(props) {
        super(props);
        this.state = { scales: props.scales };

        this.rendLeftScales = this.rendLeftScales.bind(this);
        this.rendRightScales = this.rendRightScales.bind(this);
        this.rendData = this.rendData.bind(this);
    }

    rendData(val, inv, key) {
        //console.log(this.state.scales[key]);
        let scalescpy = this.state.scales;
        scalescpy[key] = val;
        //scalescpy[key].invert = inv;
        this.setState({
                scales: scalescpy,
            },
            function() {
                this.props.rend(this.state.scales);
            }
        );
    }

    rendLeftScales() {
        var that = this;
        return Object.keys(this.props.scales).map(function(val, index) {
            if (val.startsWith('vel')) {
                return (
                    <SliderControl min = "0" max = "100" indx = { val }
                    power = { that.state.scales[val] } rend = { that.rendData }
                    name = { 'Force ' + val.slice(-1) } key={'force'+val}
                    />
                );
            }
        });
    }

    rendRightScales() {
        var that = this;
        return Object.keys(this.props.scales).map(function(val, index) {
            if (!val.startsWith('vel') && val !== 'master') {
                return (
                    <SliderControl min = "0" max = "100" indx = { val }
                    power = { that.state.scales[val] } rend = { that.rendData }
                    name = { 'Force ' + val } key={'force'+val}
                    />
                );
            }
        });
    }

    render() {
        return (
            <div className = { styles.container } >
                <div className = { styles.fullAll } >
                    <SliderControl min = "0" max = "100" key = { 'force master' } indx = { 'master' } power = { this.state.scales['master'] } rend = { this.rendData } name = { 'Force master' } />{' '}
                    <div className = { styles.halfLeft } > { this.rendLeftScales() } </div>
                    <div className = { styles.halfRight } > { this.rendRightScales() } </div>
                </div>
            </div>
        );
    }
}
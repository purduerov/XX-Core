import React, { Component } from 'react';
import SliderControl from '../SliderControl/SliderControl.jsx';
import styles from './ForceScales.css';

/*
    <SliderControl min='0' max='100' key={'thrust0'} indx={0} val={this.props.scales[0]} inv={this.props.inv[0]} rend={this.rendData.bind(this)} name={"Thruster 0"} />
*/

export default class ForceScale extends Component {
    constructor(props) {
        super(props);

        this.rendLeftScales = this.rendLeftScales.bind(this);
        this.rendRightScales = this.rendRightScales.bind(this);
        this.rendData = this.rendData.bind(this);
    }

    rendData(val, inv, key) {
        //console.log(this.props.scales[key]);
        let scalescpy = this.props.scales;      //props aren't
        scalescpy[key] = val;
        //scalescpy[key].invert = inv;
        this.props.rend(scalescpy);
    }

    rendLeftScales() {
        return Object.keys(this.props.scales).map((val, index) => {
            if (val.startsWith('vel')) {
                return (
                    <SliderControl min="0" max="100" indx={ val }
                        power={ this.props.scales[val] } rend={ this.rendData }
                        name={ 'Force '+val.slice(-1) } key={ 'force'+val }
                    />
                );
            }
        });
    }

    rendRightScales() {
        return Object.keys(this.props.scales).map((val, index) => {
            if (!val.startsWith('vel') && val !== 'master') {
                return (
                    <SliderControl min="0" max="100" indx={ val }
                        power={ this.props.scales[val] } rend={ this.rendData }
                        name={ 'Force '+val } key={ 'force'+val }
                    />
                );
            }
        });
    }

    render() {
        return (
            <div className={ styles.container } >
                <div className={ styles.fullAll } >
                    <SliderControl min="0" max="100" key={ 'force master' } indx={ 'master' } power={ this.props.scales['master'] } rend={ this.rendData } name={ 'Force master' } />
                    <div className={ styles.halfLeft } > { this.rendLeftScales() } </div>
                    <div className={ styles.halfRight } > { this.rendRightScales() } </div>
                </div>
            </div>
        );
    }
}

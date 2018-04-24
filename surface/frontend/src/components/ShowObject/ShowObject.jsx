import React, { Component } from 'react';
import styles from "./ShowObject.css";

let that;

/*
    <SliderControl min='0' max='100' key={'thrust0'} indx={0} val={this.state.scales[0]} inv={this.state.inv[0]} rend={this.rendData.bind(this)} name={"Thruster 0"} />
*/

export default class ShowObject extends Component {

    constructor(props) {
        super(props);

        this.rendObj = this.rendObj.bind(this);

        that = this;
    }

    rendChild(obj, parent_key) {
        return Object.keys(obj).map((val, index) => {
                    return (
                      <li key={parent_key+"_"+val} className={styles.center}>
                        {index != 0 && <hr className={styles.squashed}/>}
                        <span className={styles.halfLeft}>{val}:</span>
                        <span className={styles.halfRight}>{obj[val]}</span>
                      </li>
                    );
                });
    }

    rendObj() {
        return Object.keys(this.props.obj).map((val, index) => {
            if(typeof this.props.obj[val] == 'object') {
                return (
                  <div key={val} className={styles[val]}>
                    <div key={val} className={styles.openCenter}>
                      <span>{val}</span>
                      <hr className={styles.squashed}/>
                      <ul className={styles.offLeft}>
                        {this.rendChild(this.props.obj[val])}
                      </ul>
                    </div>
                    <hr/>
                  </div>
                );
            } else {
                var obj = {};
                obj[val] = this.props.obj[val];
                return (
                  <div key={val} className={styles[val]}>
                    <div className={styles.openCenter}>
                      <ul>
                        {this.rendChild(obj)}
                      </ul>
                    </div>
                    <hr/>
                  </div>
                );
            }
                });
    }

    render() {
        return (
            <div className={styles.container}>
                <div>
                    {this.rendObj()}
                </div>
            </div>
        );
    }
}

import React, { Component } from 'react';
import styles from "./Timer.css";


export default class Timer extends Component {

    constructor(props) {
        super(props);

        this.state = {start: {val: 0.00, on: false}, pause: {val: 0.00, on: false}, show: 0};
        this.cpy = {start: {val: 0.00, on: false}, pause: {val: 0.00, on: false}, show: 0};

        this.clickStart = this.clickStart.bind(this);
        this.clickPause = this.clickPause.bind(this);
        this.clickRestart = this.clickRestart.bind(this);
        this.genNumber = this.genNumber.bind(this);
        //console.log(props.disable);
    }

    clickStart() {
        if (!this.state.start.on) {
            this.cpy.start.on = true;
            this.cpy.pause.on = false;
            this.cpy.start.val = Date.now();

            this.setState(this.cpy);
        }
    }

    clickPause() {
        if(this.state.start.val != 0.00) {
            if(!this.state.pause.on && this.state.start.on) {
                this.cpy.pause.val = this.cpy.show;
                this.cpy.pause.on = true;
                this.cpy.start.on = false;

                this.setState(this.cpy);
            } else {
                this.cpy.start.on = true;
                this.cpy.pause.on = false;
                this.cpy.start.val = Date.now();
            }

            this.setState(this.cpy);
        }
    }

    clickRestart() {
        this.cpy.start.val = 0.00;
        this.cpy.start.on = false;
        this.cpy.pause.val = 0.00;
        this.cpy.pause.on = false;

        this.setState(this.cpy);
    }

    genNumber() {
        if (this.state.start.on) {
            this.cpy.show = ((Date.now() - this.cpy.start.val) / 1000 + this.cpy.pause.val);
        
        } else if (this.state.pause.on) {
            this.cpy.show = this.cpy.pause.val;
        
        } else {
            this.cpy.show = 0.00;
        
        }

        this.cpy.show = this.cpy.show > 900 ? 900 : this.cpy.show;

        this.setState(this.cpy, () => {
            console.log(this.state);
            setTimeout(this.genNumber, 30);
        });
    }

    pad(val) {
        if (typeof val == "number") {
            val.toFixed(0);
        }

        if (val.length == 1 || val.length == 4) {
            val = "0"+val;
        }

        return val;
    }

    render() {
        return (
            <div className={styles.container}>
                <div className={styles.count} >
                    <p className={styles.number+(this.state.show>840?" text-danger":
                            (this.state.show>600?" text-warning":" text-white"))}>
                                {this.pad(Math.floor(this.state.show / 60))+":"+this.pad((this.state.show % 60).toFixed(2))}
                    </p>
                </div>
                <div className={styles.buttons}>
                    <button onClick={this.clickStart}>Start</button>
                    <button onClick={this.clickPause}>Pause</button>
                    <button onClick={this.clickRestart}>Restart</button>
                </div>
            </div>
        );
    }

    componentDidMount() {
        this.genNumber();
    }

}
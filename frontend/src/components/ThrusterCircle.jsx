import React, { Component } from 'react';
import Camera from 'react-camera';


export default class ThrusterCircle extends Component {

  constructor(props) {
    super(props);
    
  }

  render() {
    return (
        <div className={this.props.className}>
            <div className={"c100 "+"p"+this.props.val+" thruster-off "+
                (this.props.val > 70? 'thruster-red' : this.props.val > 55? 'thruster-orange' : 'thruster-green')}>
                <span>{this.props.val}%</span>
                <div className="slice">
                    <div className="bar"></div>
                    <div className="fill"></div>
                </div>
            </div>
        </div>
    );
  }
}
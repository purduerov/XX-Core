import React, { Component } from 'react';
import Camera from 'react-camera';


export default class ThrusterCircle extends Component {

  constructor(props) {
    super(props);
    this.state = {'on': null};
    this.state.on = 0+(!props.disabled);

    this.onClick = this.onClick.bind(this);
  }

  onClick(e) {
      this.setState({
          on: 0+(!this.state.on)
      });

      console.log(this.state.on);
      this.props.rend(this.state.on, this.props.indx);
  }

  render() {
    return (
        <div className={this.props.className}>
            <div className={this.state.on===1?("c100 "+"p"+this.props.val+" select thruster-off "+
                (this.props.val > 70? 'thruster-red' : this.props.val > 55? 'thruster-orange' : 'thruster-green')):
                "c100 "+"p"+this.props.val+" thruster-off thruster-grey"} onClick={this.onClick}>
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
import React, { Component } from 'react';


export default class ThrusterCircle extends Component {

  constructor(props) {
    super(props);

    this.onClick = this.onClick.bind(this);
    //console.log(props.disable);
  }

  onClick(e) {
    this.props.rend(!this.props.disable, this.props.indx);
  }

  render() {
    return (
        <div className={this.props.className}>
            <div className={"c100 p"+this.props.val+" thruster-off " + (this.props.disable === false?("select "+ //thrusters
                (this.props.val > 70? 'thruster-red' : this.props.val > 55? 'thruster-orange' : 'thruster-green')):
                "thruster-grey")} onClick={this.onClick}>
                <span>{this.props.val.toFixed(2)}%</span>
                <div className="slice">
                    <div className="bar"></div>
                    <div className="fill"></div>
                </div>
            </div>
        </div>
    );
  }

}

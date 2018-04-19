import React, { Component } from 'react';


export default class ThrusterCircle extends Component {

  constructor(props) {
    super(props);
    this.state = {off: 0+(props.disable)};

    this.onClick = this.onClick.bind(this);
    //console.log(props.disable);
  }

  onClick(e) {
      this.setState(function(state, props) {
          return {off: (1-state.off)}
      }, function() {
        this.props.rend(this.state.off, this.props.indx);
        //console.log(this.state.off);
      });
  }

  render() {
    return (
        <div className={this.props.className}>
            <div className={"c100 "+"p"+this.props.val+" select thruster-off "+ //tools
              (this.props.val > 0? 'thruster-green' : this.props.val < 0? 'thruster-red' : 'thruster-grey') }>
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

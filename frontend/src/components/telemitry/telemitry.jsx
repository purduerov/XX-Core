//to test, go to dev, index.jsx is where you include this. Put this into the camera window, titles "camera view" or "camera window"
//-z down from rov, positive x off nose of plane, y out sides of rov
import React, { Component } from 'react';
import styles from "./telemitry.css";

class telemetryComponent extends React.Component {
	var deltapxyaw;
	var deltapxpitch;
	var deltapxroll;
	var prevyaw;
	var prevpitch;
	var prevroll;
	constructor(props) {
		super(props);
		this.state = {'roll': props.roll, 'pitch': props.pitch, 'yaw': props.yaw, 'camW': props.camW, 'camH': props.camH} // DOES WINDOW WIDTH AND HEIGHT NEED TO GO IN HERE?
	}
	render() {
		return (
			<canvas ref="horizCanv"  left={deltapxyaw}> </canvas>
			<canvas ref="vertCanv"  top={deltapxpitch}></canvas>
			<canvas ref="rollCanv" transform: rotate({props.roll})></canvas>
		)
	}


	componentWillMount() {

	}


	componentDidMount() {
		let horizCanv = ReactDOM.findDOMNode(this.refs.horizCanv);
		horizCanv.width = wWidth * (360 / this.props.camFeedWidthDeg);
		horizCanv.height = 100%;
		horizeCanv.position="relative";
		let vertCanv = ReactDOM.findDOMNode(this.refs.vertCanv);
		vertCanv.width = wWidth;
		vertCanv.height = wHeight * (360 / this.props.camFeedHeightDeg);
		vertCanv.position = "relative";
		const horizctx = horizCanv.getContext("2d");
		const vertctx = vertCanv.getContext("2d");
		var yawincr = horizCanv.width * 1/14;
		var pitchincr = vertCanv.height * 1/14;
		var currpx = 0;
		var flatpixhoriz = 3/14 * horizCanv.width - ($(window).height() / 2);
		var flatpixvert = 3/14 * horizCanv.width - ($(window).width() / 2);

		//this section draws tick marks for the yaw
		var cardinalDir = "W";
		var subCardinalDir = "SW";
		ctx.font = "20px Comic Sans";
		for(currpx = -3 * yawincr; currpx < horizCanv.width; currpx += yawincr) {
			if(currpx % 90 == 0) { //this is wrong
				ctx.beginPath();
				ctx.moveTo(currpx + 3 * yawincr, 0);
				ctx.lineTo(currpx + 3 * yawincr, 30);
				if (cardinalDir == "N") {
					ctx.fillText(cardinalDir, currpx + 3 * yawincr, 55);
					cardinalDir = "E";
				}
				else if (cardinalDir == "E") {
					ctx.fillText(cardinalDir, currpx + 3 * yawincr, 55);
					cardinalDir = "S";
				}
				else if (cardinalDir == "S") {
					ctx.fillText(cardinalDir, currpx + 3 * yawincr, 55);
					cardinalDir = "W"
				}
				else if (cardinalDir == "W") {
					ctx.fillText(cardinalDir, currpx + 3 * yawincr, 55);
					cardinalDir = "N";
				}
			}
			else if (currpx % 45 == 0)  {
				ctx.beginPath();
				ctx.moveTo(currpx + 3 * yawincr, 0);
				ctx.lineTo(currpx + 3 * yawincr, 45);
				if (subCardinalDir == "SW") {
					ctx.fillText(subCardinalDir, currpx + 3 * yawincr, 55);
					subCardinalDir = "NW";
				}
				else if (subCardinalDir == "NW") {
					ctx.fillText(subCardinalDir, currpx + 3 * yawincr, 55);
					subCardinalDir = "NE";
				}
				else if (subCardinalDir == "NE") {
					ctx.fillText(subCardinalDir, currpx + 3 * yawincr, 55);
					subCardinalDir = "SE"
				}
				else if (subCardinalDir == "SE") {
					ctx.fillText(subCardinalDir, currpx + 3 * yawincr, 55);
					subCardinalDir = "SW";
				}
			}

			ctx.beginPath();
			ctx.moveTo(currpx + 3 * yawincr, 0);
			ctx.lineTo(currpx + 3 * yawincr, 15);
		}


		//this section draws the pitch
		currpx = 0;
		for(currpx = -3 * pitchincr; currpx < vertCanv.height; currpx += pitchincr) {
			if(currpx % 90 == 0) { //this is wrong
				ctx.beginPath();
				ctx.moveTo(0, currpx + 3 * pitchincr);
				ctx.lineTo(30, currpx + 3 * pitchincr);

			}
			else if (currpx % 45 == 0)  {
				ctx.beginPath();
				ctx.moveTo(0, currpx + 3 * pitchincr);
				ctx.lineTo(45, currpx + 3 * pitchincr);
			}
		}
		ctx.beginPath();
		ctx.moveTo(0, currpx + 3 * pitchincr);
		ctx.lineTo(15, currpx + 3 * pitchincr);
	}


	componentWillUpdate() {
		//let horizCanv = ReactDOM.findDOMNode(this.refs.horizCanv);
		//let vertCanv = ReactDOM.findDOMNode(this.refs.vertCanv);
		this.deltapxyaw = (this.props.yaw - prevyaw) * horizCanv.width / 630;
		this.deltapxpitch = (this.props.pitch - prevpitch) * vertCanv.height / 630;
		this.deltapxroll = (this.props.roll - prevroll);
	}
})

module.exports = {
    dearflask: {
        thrusters: {
            desired_thrust: [
                0, // x:     forwards and backwards
                0, // y:     strafe left or right
                0, // z:     ascend / descend
                0, // roll:  roll to the left or right
                0, // pitch: nose up or down
                0 // yaw:    left or right rotation
            ],
            frozen: [
                0, // x:     forwards and backwards
                0, // y:     strafe left or right
                0, // z:     ascend / descend
                0, // roll:  roll to the left or right
                0, // pitch: nose up or down
                0 // yaw:    left or right rotation
            ],
            disabled_thrusters: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            thruster_scales: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        },
        claw: {
            power: 0.0
        },
        cameras: {},
        leds: {
            bluetooth_led: false,
            camera_leds: false
        },
        maincam_angle: 0.0,
        last_update: ""
    },
    dearclient: {
	      imu: {
		        acceleration:{
			          y:0,
			          x:0,
			          z:0
		        },
            gyro:{
			          y:0,
			          x:0,
			          z:0
		        },
		        euler:{
			          yaw:0,
			          roll:0,
			          pitch:0
		        },
		        temp:0,
		        linear_acceleration:{
			          y:0,
			          x:0,
			          z:0
		        }
        },
        pressure: {
            pressure: 7,
            temperature: 4
        },
        obs: {
             tilt: {
                x:0.0,
                y:0.0,
                z:0.0
             },
             seismograph_data: {
                time: [0.0,0.1,0.2],
                amplitude: [0.0,0.2,0.4]
             }
        },                
        esc: {
             currents: [0.1,0.2],
             temperatures: [0.0,0.1]
        },
        last_update: "",
        frozen: {
            x: false,
            y: false,
            z: false,
            pitch: false,
            roll: false,
            yaw: false
        },
        thrusters: [.0, .0, .0, .0, .0, .0, .0, .0]
    }
};

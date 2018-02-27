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
        }
    },
    dearclient: {
	last_update: 0.0
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
		linear-acceleration:{
			y:0,
			x:0,
			z:0
		}
        },
        frozen: {
            x: false,
            y: false,
            z: false,
            pitch: false,
            roll: false,
            yaw: false
        },
        thrusters: [.0, .0, .0, .0, .0, .0, .0, .0],
    }
};

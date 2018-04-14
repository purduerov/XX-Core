from numpy import linalg
import numpy as np
import pprint as pp
from rov import init_hw_constants


class Complex():
    """
    This code is a rewrite of MutatorMatrix to simplify and clarify the code without removing the source
    This thrust-mapping works by solving the least squared solution of a system determined by the thrusters locations
    and the directions of the thrusters.
    The system is the 6x8 matrix made of columns of each thrusters affect on each component X, Y, Z. ROLL, PITCH, YAW
    multiplied by the 8x1 thrust map matrix (which we are solving for) equal to the 6x1 desired thrust matrix
    To find the least square solution we find the pseudo-inverse of the 6x8 matrix (A) and multiply both sides of the
    equation by it. If a inverse of the matrix A exists the pseudo-inverse(A) = inverse(A) if not then
    pseudo-inverse(A) * A can be ignored because math leaving
    thrust map matrix = pseudo-inverse(A) * desired thrust
    For location and rotation vectors, the first four thrusters are the horizontal thrusters: first is front left,
    second is front right, third is back left, and fourth is back right. The last four are the vertical thrusters in
    the same order: front left, front right, back left, and back right.
    Outside classes use this class to find the pwm values for each thruster based on force input. The _calculate
    function returns the 8D pwm vector for the thrusters, and the _get_results function returns the force vector based
    on the pwm vector. The thrust and power output of each thruster are in the arrays thrust and power, and the total
    power can be accessed with the variable final_power.
    """
    # XX Thruster locations and center of mass relative to an arbitrary(?) point converted from inches to meters
    # Each column is X, Y, Z: X is forward/back, Y is left/right, Z is up/down
    XX_THRUSTERS = np.matrix([
        [6.7593, 6.7593, -6.7593, -6.7593, 7.6887, 7.6887, -7.6887, -7.6887],
		[-6.625, 6.625, -6.625, 6.625, -3.75, 3.75, -3.75, 3.75],
        [-0.5809, -0.5809, -0.5809, -0.5809, 4.8840, 4.8840, 4.8840, 4.8840]
    ]) * 0.0254

    XX_COM = np.matrix([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]) * 0.0254

    # X and Y component of horizontal thrusters converted to radians to be used by numpy 7pi/18 rad = 70 degrees
    X_COMPONENT = np.sin(7 * np.pi / 18)
    Y_COMPONENT = np.cos(7 * np.pi / 18)

    ROTATION = np.matrix([
        [X_COMPONENT, X_COMPONENT, -X_COMPONENT, -X_COMPONENT, 0, 0, 0, 0],
        [Y_COMPONENT, -Y_COMPONENT, Y_COMPONENT, -Y_COMPONENT, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1]
    ])

    def __init__(self):
        self.thruster_layout = np.matrix(Complex.XX_THRUSTERS - Complex.XX_COM)
        # this is the 6x8 matrix that specifies each thrusters contribution on X, Y, Z, Roll, Pitch, Yaw
        self.matrix = None
        # the pseudo inverse of self.matrix used to find the least square solution
        self.pseudo_inverse_matrix = None
        # list of disabled thrusters used to determine when matrix and pseudo_inverse_matrix need to be updated
        self.disabled = [0, 0, 0, 0, 0, 0, 0, 0]
        # The last thrust map returned by the calculate function
        self.map = None

        self.thrust = np.matrix([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.power = np.matrix([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.final_power = 0.0

        self._generate_matrix()

    def calculate(self, desired_thrust, disabled_thrusters=None, disable_limiting=False):
        """
        Calculate the needed thrust for each thruster to achieve desired
        :param desired_thrust: The 6 dimensional vector which we want to achieve vector as 6x1 matrix
        :param disabled_thrusters: list of 8 items each corresponding to a thruster (0 meaning enabled, 1 disabled)
        :return: the thrust map generated by solving for the least square solution of the equation
        """
        # In the case of a thruster malfunction this allows for the pseudo_inverse_matrix to be recalculated
        # to account for the thruster that no longer works
        if disabled_thrusters != self.disabled:
            self.disabled = disabled_thrusters
            self._generate_matrix()

        #print desired_thrust

        self.map = self.pseudo_inverse_matrix.dot(desired_thrust)

        self._normalize(desired_thrust)
        initial_power, limitPower = self._calc_thrust_power(self.map)
        #limit power if necessary:
        self.final_power = initial_power
        iteration = 0
        while limitPower == 1 and disable_limiting == False:
            if iteration > 3:
                print('Limit power function iteration limit exceeded, assume values are close enough.')
                break
            self.final_power = self._limit_power(initial_power)
            self.final_power, limitPower = self._calc_thrust_power(self.map)
            print('Power was limited, force vector changed!')
        return self.map.tolist()[0]

    def _generate_matrix(self):
        """
        Generate the pseudo-inverse of the matrix to be used in the calculation
        :return: the pseud-inverse of self.matrix
        """
        # Calculate the cross product between the location of each thruster and the direction it points in
        rot = np.transpose(np.cross(np.transpose(self.ROTATION), np.transpose(self.thruster_layout), 1))
        self.matrix = np.concatenate((self.ROTATION, rot))
        for thruster in range(8):
            if self.disabled[thruster]:
                self.matrix[:, thruster] = 0.0
        self.pseudo_inverse_matrix = linalg.pinv(self.matrix)
        return self.pseudo_inverse_matrix

    def _normalize(self, desired_thrust):
        """
        Normalize the values of the thrust map to be in the range [-max input force, max input force]
        :return: None
        """
        max_val = np.amax(np.abs(self.map))
        
        max_force = np.amax(np.abs(desired_thrust))

        self.map *= (max_force/max_val)

    def _limit_power(self, initialPower):
        """
        Ensure power limit is not exceeded by scaling the thruster values down if necessary
        :return: limitedPower
        """
        limitedPower = 0.0
        #initialize maxPower as lowest power value
        maxPower = 0.51
        maxPowerIndex = 0
        for thruster in range(8):
            if self.power[0, thruster] > maxPower:
                maxPower = self.power[0, thruster]
                maxThrust = self.thrust[0, thruster]
                maxPowerIndex = thruster
        orig_thrust_maxP = maxThrust;
        self.thrust[0, maxPowerIndex] = self._power_to_thrust(init_hw_constants.POWER_THRESH, orig_thrust_maxP)
        overMaxPower = np.matrix([0, 0, 0, 0, 0, 0, 0, 0])
        # find thrusters with over power threshold and make them the threshold value based on PWM value and
        # mark which were changed
        for thruster in range(8):
            if self.thrust[0, thruster] < 0:
                while self._pwm_to_power(self.map[0, thruster]) > init_hw_constants.POWER_THRESH:
                    self.map[0, thruster] = self.map[0, thruster] + 0.005
                    overMaxPower[0, thruster] = 1
            if self.thrust[0, thruster] > 0:
                while self._pwm_to_power(self.map[0, thruster]) > init_hw_constants.POWER_THRESH:
                    self.map[0, thruster] = self.map[0, thruster] - 0.005
                    overMaxPower[0, thruster] = 1
            if thruster == maxPowerIndex:
                self.thrust[0, maxPowerIndex] = self._power_to_thrust(self._pwm_to_power(self.map[0, thruster]), orig_thrust_maxP)
        # change thrust values to
        for thruster in range(8):
            if thruster != maxPowerIndex:
                self.thrust[0, thruster] = self.thrust[0, thruster] * self.thrust[0, maxPowerIndex] / orig_thrust_maxP
                self.power[0, thruster] = self._thrust_to_power(self.thrust[0, thruster])
            limitedPower = limitedPower + self.power[0, thruster]
            if overMaxPower[0, thruster] != 1:
                self.map[0, thruster] = self._thrust_to_pwm(self.thrust[0, thruster])
        return limitedPower

    def _calc_thrust_power(self, thrusters):
        """
        Find the total power used by all 8 thrusters for given pwm values
        Also calculate the thrust and power for each individual thruster for global variables
        :return: totalPower, limitPower
        """
        # calculate thrust output and power used values for each thruster
        totalPower = 0.0
        limitPower = 0
        for thruster in range(8):
            pwm_output = thrusters[0, thruster]
            self.thrust[0, thruster] = self._pwm_to_thrust(pwm_output)
            self.power[0, thruster] = self._pwm_to_power(pwm_output)
            totalPower = totalPower + self.power[0, thruster]
            # set flag to limit power if any use more than allocated threshold value (based on power design)
            if self.power[0, thruster] > init_hw_constants.POWER_THRESH:
                limitPower = 1
        return totalPower, limitPower

    def _pwm_to_thrust(self, pwm):
        """
        Change PWM value to thrust value based on 12V data from thrusters
        :return: Thrust Value (lbf)
        """
        if pwm < -0.05:
            thrustVal = -3.6529*(pwm**3)-9.8279*(pwm**2)+0.5183*pwm-0.04
        elif pwm > 0.05:
            thrustVal = -5.9996*(pwm**3)+13.296*(pwm**2)+0.4349*pwm+0.0345
        else:
            thrustVal = 0
        return thrustVal

    def _pwm_to_power(self, pwm):
        """
        Convert PWM value to power value based on 12V data from thrusters
        :return: Power Value (W)
        """
        if pwm < 0:
            powerVal = -53.282*(pwm**3)+135.58*(pwm**2)+1.1986*pwm+0.51
        else:
            powerVal = 35.949*(pwm**3)+150.51*(pwm**2)-3.0096*pwm+0.51
        return powerVal

    def _power_to_thrust(self, powerVal, sign):
        """
        Convert power value to thrust value based on 12V data from thrusters, given desired sign of thrust
        Note that sign can be any positive or negative value, or 0 if thrust is zero
        :return: thrust value (lbf)
        """
        if sign > 0:
            thrustVal = 0.000001*(powerVal**3)-0.0004*(powerVal**2)+0.0855*powerVal
        elif sign < 0:
            thrustVal = -0.0000008*(powerVal**3)+0.0003*(powerVal**2)-0.0697*powerVal
        else:
            thrustVal = 0;
        return thrustVal

    def _thrust_to_power(self, thrustVal):
        """
        Convert thrust value to power value based on 12V data from thrusters
        :return: power value (W)
        """
        if thrustVal < 0:
            powerVal = 2.3329*(thrustVal**2)-12.016*thrustVal+0.0959
        if thrustVal > 0:
            powerVal = 1.8977*(thrustVal**2)+8.37*thrustVal+1.2563
        else:
            powerVal = 0.51;
        return powerVal

    def _thrust_to_pwm(self, thrustVal):
        """
        Convert thrust value to PWM value based on 12V data from thrusters
        :return: PWM value
        """
        if thrustVal < 0:
            pwm = 0.0021*(thrustVal**3)+0.0298*(thrustVal**2)+0.2426*thrustVal-0.0775
        elif thrustVal > 0:
            pwm = 0.0017*(thrustVal**3)-0.025*(thrustVal**2)+0.213*thrustVal+0.0675
        else:
            # assume 0 even though dead band has range of pwm values
            pwm = 0;
        return pwm;

    def _get_results(self):
        """
        Method for returning what the resulting thrust map would cause for the rov based
        on the thruster locations and angles.
        N.B. the normalize function can cause these values to be radically different than the intended. Disable it
             in the calculate function to get more accurate results. If normalized it should be correct just scaled down
        :return: dict of X, Y, Z, Roll, Pitch, Yaw
        """
        res = c.matrix * np.transpose(c.map)
        result = {
            'X': res[0, 0],
            'Y': res[1, 0],
            'Z': res[2, 0],
            'Roll': res[3, 0],
            'Pitch': res[4, 0],
            'Yaw': res[5, 0]
        }
        return result


if __name__ == '__main__':
    c = Complex()
    np.set_printoptions(linewidth=150, suppress=True)
    print('MATRIX')
    pp.pprint(c.matrix)
    print('\nPSEUDO-INVERSE MATRIX')
    pp.pprint(c.pseudo_inverse_matrix)
    print('\nRESULT 8D VECTOR')
    pp.pprint(c.calculate(np.array([1, 0, 0, 0, 0, 0]), [0, 0, 1, 0, 0, 0, 0, 0], False))
    print('\nTHRUST')
    pp.pprint(c.thrust)
    print('POWER')
    pp.pprint(c.power)
    print('\nTOTAL POWER')
    pp.pprint(c.final_power)
    print('\nRESULTING 6D VECTOR')
    pp.pprint(c._get_results())

import pytest
from rov.movement.thruster.Force_Limiter import *

"""
def test_thrust_limiter():  // for testing assert
    assert 1 == 1
"""

# comments need to be fixed


def test_check_if_reach_arbitrary_speed_from_zero_speed():
    """
            speed: zero -> nonzero (all +)
            ramp_by: 0.01
    """
    
    limiter = ThrustLimiter()
    # print "limiter speed", limiter.speed

    limiter.speed = [0 for _ in range(8)]
    # hard-coded desired speed
    new_speed = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

    # as long as desired speed != current speed
    while limiter.speed != new_speed:
        limiter.speed = limiter.ramp(new_speed, 0.02)   # setting inc_ramp_by to 0.02, ramp_by == 0.01
        # print limiter.speed

    assert limiter.speed == new_speed


def test_check_if_reach_zero_speed_from_nonzero_speed():
    """
        speed: nonzero (+ & -) -> 0
        ramp_by: 0.05
    """
    limiter = ThrustLimiter()
    # print "limiter speed", limiter.speed

    limiter.speed = [-1, -0.7, 0.5, 0.8, 0.1, 0, -0.4, 0.01]
    # hard-coded desired speed
    new_speed = [0 for _ in range(8)]

    # as long as desired speed != current speed
    while limiter.speed != new_speed:
        limiter.speed = limiter.ramp(new_speed, 0.1)
        # print "\nselfspeed: ", limiter.speed

        # print "\ndesiredspeed: ", limiter.desired_speed
        # print "\nrampingspeed: ", limiter.ramp_by

    assert limiter.speed == new_speed


def test_check_if_reach_negative_and_positive_arbitrary_speed_from_zero_speed():
    """
        speed: 0 -> nonzero (+ & -)
        ramp_by: 0.05
    """
    limiter = ThrustLimiter()
    # print "limiter speed", limiter.speed

    limiter.speed = [0 for _ in range(8)]
    # hard-coded desired speed
    new_speed = [-1, -0.5, 1, 0.5, -0.3, 0.3, 0, -0.8]

    # as long as desired speed != current speed
    while limiter.speed != new_speed:
        limiter.speed = limiter.ramp(new_speed, 0.1)
        # print limiter.speed

    assert limiter.speed == new_speed


def test_check_if_reach_min_speed_from_max_speed():
    """
        speed: +1 -> -1
        ramp_by: 0.275
    """
    limiter = ThrustLimiter()
    # print "limiter speed", limiter.speed

    limiter.speed = [1 for _ in range(8)]
    # hard-coded desired speed
    new_speed = [-1 for _ in range(8)]

    # as long as desired speed != current speed
    while limiter.speed != new_speed:
        limiter.speed = limiter.ramp(new_speed, 0.55)
        # print limiter.speed

    assert limiter.speed == new_speed


def test_check_if_reach_max_speed_from_min_speed():
    """
        speed: -1 -> +1
        ramp_by: 0.275
    """
    limiter = ThrustLimiter()
    # print "limiter speed", limiter.speed

    limiter.speed = [-1 for _ in range(8)]
    # hard-coded desired speed
    new_speed = [1 for _ in range(8)]

    # as long as desired speed != current speed
    while limiter.speed != new_speed:
        limiter.speed = limiter.ramp(new_speed, 0.55)
        # print limiter.speed

    assert limiter.speed == new_speed


def test_check_if_reach_arbitrary_speed_from_zero_speed_back_to_zero_speed():
    """
        speed 0 -> speed 1 (for 10 loops) -> speed 0
        ramp_by: 0.25 -> 0.10
    """
    limiter = ThrustLimiter()
    # print "limiter speed", limiter.speed

    limiter.speed = [0 for _ in range(8)]
    # hard-coded desired speed
    new_speed = [1 for _ in range(8)]

    # as long as desired speed != current speed
    for _ in range(10):
        limiter.speed = limiter.ramp(new_speed, 0.5)
        # print limiter.speed

    new_speed = [0 for _ in range(8)]

    while limiter.speed != new_speed:
        limiter.speed = limiter.ramp(new_speed, 0.2)
        # print limiter.speed

    assert limiter.speed == new_speed

def test_check_if_reach_arbitrary_speed_from_max_speed_back_to_max_speed():
    """
        ramp_by: 0.25 -> 0.10
        starting speed = 1 (for all motors)
        goal speed = -1 (for all motors, 10 loops)
        updated goal speed = 1 (for all motors)
    """
    limiter = ThrustLimiter()
    # print "limiter speed", limiter.speed

    limiter.speed = [1 for _ in range(8)]
    # hard-coded desired speed
    new_speed = [-1 for _ in range(8)]

    # as long as desired speed != current speed
    for _ in range(10):
        limiter.speed = limiter.ramp(new_speed, 0.5)

    new_speed = [1 for _ in range(8)]

    while limiter.speed != new_speed:
        limiter.speed = limiter.ramp(new_speed, 0.2)

    assert limiter.speed == new_speed


# if __name__ == "__main__":
    # test_check_if_reach_arbitrary_speed_from_zero_speed()
    # test_check_if_reach_zero_speed_from_nonzero_speed()
    # test_check_if_reach_max_speed_from_min_speed()
    # test_check_if_reach_min_speed_from_max_speed()
    # test_check_if_reach_negative_and_positive_arbitrary_speed_from_zero_speed()
    # test_check_if_reach_arbitrary_speed_from_zero_speed_back_to_zero_speed()

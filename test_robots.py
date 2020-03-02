import pytest

from robots import Asteroid, Robot, Processor



def test_robot_initial_position():

    ''' test all strings for bearings will work '''

    bearings = ['north', 'south', 'east', 'west']

    for b in bearings:
        robot = Robot(1, 2, b)
        assert robot.x == 1 and robot.y == 2 and robot.bearing == b



def test_asteroid_size_and_mode():

    ''' test asteroid sets x and y properly and sets default mode '''

    setup = [[1, 2, 'default'], [3,4, '3d'], [4,6, 'default']]

    for s in setup:
        asteroid = Asteroid(s[0], s[1], s[2])
        assert asteroid.x == s[0] and asteroid.y == s[1] and asteroid.mode == s[2]




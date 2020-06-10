# -*- coding: utf-8 -*-
''' robot tests '''
import os
import unittest
import robotsuite
from eea.restapi.testing import EEA_RESTAPI_ACCEPTANCE_TESTING  # noqa: E501
from plone.app.testing import ROBOT_TEST_LEVEL
from plone.testing import layered


def test_suite():
    ''' test suite '''
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_dir = os.path.join(current_dir, 'robot')
    robot_tests = [
        os.path.join('robot', doc) for doc in os.listdir(robot_dir)
        if doc.endswith('.robot') and doc.startswith('test_')
    ]
    for robot_test in robot_tests:
        robottestsuite = robotsuite.RobotTestSuite(robot_test)
        robottestsuite.level = ROBOT_TEST_LEVEL
        suite.addTests([
            layered(
                robottestsuite,
                layer=EEA_RESTAPI_ACCEPTANCE_TESTING,
            ),
        ])
    return suite

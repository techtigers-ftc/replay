from spike import MotorPair, ColorSensor, StatusLight, MotionSensor, Speaker, PrimeHub, Motor
from spike.control import wait_for_seconds
from .robot import Robot



class TestCase:
    def __init__(self, case_id, test, expected_result, actual_result, setup = None):
        """
        :param case_id: The test number
        :type case_id: Number
        :param test: Start of a test
        :type test: Number or string
        :param expected_result: The expected outcome 
        :type expcted_result: String 
        :param actual_result: The result of the test
        :type actual_result: String
        :param setup: Optional preliminary function which can be used to sateup the robot before the test has been run
        :type setup: Function

        """
     
        self.case_id = case_id
        self.test = test
        self.description = description
        self.setup = setup
        self.test = test
           
    

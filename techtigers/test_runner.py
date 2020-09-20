from spike import MotorPair, ColorSensor, StatusLight, MotionSensor, Speaker, PrimeHub, Motor
from spike.control import wait_for_seconds
from .timer import Timer
from .robot import Robot

class TestRunner:
    def __init__(self, test_cases, do_test):
        self.robot = Robot()
        self.hub = PrimeHub()
        self.timer = Timer()
        self.test_cases = test_cases
        self.do_test = do_test

    def run_test(self):
        for test_case in self.test_cases:
            # Show pattern to indicate that we are waiting for user input
            self.hub.light_matrix.show_image('DIAMOND')
            self.hub.status_light.on("azure")
            print("___________________")
            print("Waiting to start test {}".format(test_case["test"]))

            # Wait for the user to press and release the left button
            self.hub.left_button.wait_until_pressed()
            self.hub.left_button.wait_until_released()
            
            print("___________________")
            print("Starting test {}".format(test_case["test"]))
            self.hub.light_matrix.show_image("XMAS")
            print(test_case["expected_result"])

            test_case["result"] = self.do_test(test_case)

            if test_case["result"] == True:
                self.hub.light_matrix.show_image("YES")
            else:
                self.hub.light_matrix.show_image("NO")

            print("__________________")
            print("Test completed. Result: {}".format(test_case["result"]))
            wait_for_seconds(2)

        def print_results(self):
            for test_case in self.test_cases:
                print(test_case)
from spike import MotorPair, ColorSensor, StatusLight, MotionSensor, Speaker, PrimeHub, Motor
from spike.control import wait_for_seconds
from .timer import Timer
from .robot import Robot

class TestRunner:
    def __init__(self, test_cases, do_test, setup = None):
        self.robot = Robot()
        self.hub = PrimeHub()
        self.timer = Timer()
        self.test_cases = test_cases
        self.do_test = do_test
        self.arr = []
        self.setup = setup
    
    def run_test(self):
        for test_case in self.test_cases:
            # Show pattern to indicate that we are waiting for user input
            if self.setup != None:
                self.setup(self.robot, test_case)
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

            test_case["result"] = self.do_test(self.robot, test_case)

            if test_case["result"] == True:
                self.hub.light_matrix.show_image("YES")
            else:
                self.hub.light_matrix.show_image("NO")

            print("__________________")
            print("Test completed. Result: {}".format(test_case["result"]))
            self.robot.drift_check()

    def print_results(self):
        lines = []
        for item in self.test_cases:
            line = []
            for key in item:
                line.append(str(item[key]))
            lines.append(','.join(line))

        raw_results ="\\n".join(lines)
        print("python -c 'print(\"{}\")'".format(raw_results))


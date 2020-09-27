from .robot import Robot
from spike.control import wait_for_seconds

class TestRunner:
    def __init__(self, test_cases):
        """ A class that is used to test navigation functions

        :param test_cases: An array that contains the info for tests
        :type test_cases: Array
        """
        self.robot = Robot()
        self.hub = self.robot.hub
        self.test_cases = test_cases
    
    def run_test(self):
        # TODO: Comment This!!!
        for test_case in self.test_cases:
            print("Running setup for test {}".format(test_case.case_id))
            self.hub.light_matrix.show_image('CHESSBOARD')
            self.hub.status_light.on("cyan")

            if test_case.setup != None:
                test_case.setup(self.robot, test_case)

            print("Waiting to start test {}".format(test_case.case_id))
            self.hub.light_matrix.show_image('DIAMOND')
            self.hub.status_light.on("azure")

            # Wait for the user to press and release the left button
            self.robot.wait_left_button()
            
            print("Starting test {}".format(test_case.case_id))
            self.hub.light_matrix.show_image("CONFUSED")
            print(test_case.description)

            test_case.result = test_case.do_test()

            if test_case.result == True:
                self.hub.light_matrix.show_image("YES")
            else:
                self.hub.light_matrix.show_image("NO")

            print("Test completed. Result: {}".format(test_case.result))
            print("__________________")
            wait_for_seconds(1)

    def print_results(self):
        # TODO: Comment This!!!
        lines = []
        for test_case in self.test_cases:
            lines.append(test_case.get_csv())

        raw_results ="\\n".join(lines)
        print("python -c 'print(\"{}\")'".format(raw_results))


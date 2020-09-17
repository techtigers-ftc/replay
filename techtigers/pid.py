from .timer import Timer

class Pid:
    def __init__(self, kp, ki, kd):
        """Class that can be used to do PID calculations.

        :param kp: Proportional multiplier for the error
        :type kp: Number
        :param ki: Multiplier for the intergral of the error
        :type ki: Number
        :param kd: Multiplier for the derivative of the error
        :type kd: Number
        """
        self.clock = Timer()
        self.kp = kp
        self.ki = ki / 100000
        self.kd = kd
        self.last_error = 0
        self.total_error = 0

    def reset(self):
        """Reset parameters before start of PID loop
        """
        self.clock.reset()
        self.last_error = 0
        self.total_error = 0

    def compute_steering(self, error):
        """Computes and returns the corrections.

        :param error: Difference between target and actual angles
        :type error: Number
        :return: Returns correction value
        :rtype: Number
        """
        elapsed_time = self.clock.duration() / 1000
        error_change = 0

        if elapsed_time > 0:
            error_change = (error - self.last_error)/elapsed_time
            self.total_error = self.last_error * elapsed_time + self.total_error

        self.last_error = error

        steering = max(min(error * self.kp, 100), -100)
        steering += max(min(error_change * self.kd, 100), -100)
        steering += max(min(self.total_error * self.ki, 100), -100)
        steering = max(min(steering / 1.8, 100), -100)

        return int(-steering)

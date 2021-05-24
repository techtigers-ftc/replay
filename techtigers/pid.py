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
        # --- TEMP CODE START ---
        self._error_change_min = 1000000
        self._error_change_max = -1000000
        self._error_change_total = 0

        self._total_error_min = 1000000
        self._total_error_max = -1000000
        self._total_error_total = 0

        self._iterations = 0
        # --- TEMP CODE END ---

    def reset(self):
        """Reset parameters before start of PID loop
        """
        self.clock.reset()
        self.last_error = 0
        self.total_error = 0
        # --- TEMP CODE START ---
        self._error_change_min = 1000000
        self._error_change_max = -1000000
        self._error_change_total = 0

        self._total_error_min = 1000000
        self._total_error_max = -1000000
        self._total_error_total = 0

        self._iterations = 0
        # --- TEMP CODE END ---

    def compute_steering(self, error):
        """Computes and returns the corrections.

        :param error: Difference between target and actual angles
        :type error: Number
        :return: Returns correction value
        :rtype: Number
        """
        # elapsed_time = self.clock.duration() / 1000
        # error_change = 0
        # if elapsed_time > 0:

            # error_change = (error - self.last_error)/elapsed_time
            # self.total_error = self.last_error * (elapsed_time / 1000000) + self.total_error
            # --- TEMP CODE START ---
            # if error_change < self._error_change_min:
            #     self._error_change_min = error_change
            # if error_change > self._error_change_max:
            #     self._error_change_max = error_change
            # self._error_change_total += error_change

            # if self.total_error < self._total_error_min:
            #     self._total_error_min = self.total_error
            # if self.total_error > self._total_error_max:
            #     self._total_error_max = self.total_error
            # self._total_error_total += self.total_error

            # self._iterations += 1
            # --- TEMP CODE END ---

        error_change = (error - self.last_error)
        self.total_error += error

        self.last_error = error

        steering = error * self.kp
        steering += error_change * self.kd
        steering += self.total_error * self.ki

        return int(steering)

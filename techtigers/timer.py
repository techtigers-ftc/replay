import utime

class Timer:
    def __init__(self):
        """Class that implements timer at microsecond clock
        """
        self.start = utime.ticks_us()

    def reset(self):
        """Resets the timer
        """
        self.start = utime.ticks_us()

    def duration(self):
        """Returns time elapsed since last reset

        :return diff: The time elapsed since last reset
        :type diff: Number
        """
        return utime.ticks_diff(utime.ticks_us, self.start)

class Logger():
    def __init__(self):
        self._data = []
        self._counter = 0

    def log_start_pid(self, pid, speed = None, duration = None):
        self._counter = 0
        self._data.append([0, pid.kp, pid.ki, pid.kd, speed, duration])

    def log_run_pid(self, target_angle, actual_angle, correction): 
        if self._counter == 100:
            self._data.append([1, target_angle, actual_angle, correction])
            self._counter = 0
        else:
            self._counter += 1

    def stop_pid(self):
        self._data.append([2])

    def write(self):
        with open('pid_values.csv', 'a') as outfile:
            for line in self._data:
                print(line)
                outfile.write(','.join([str(item) for item in self._data]))
            self._data = []

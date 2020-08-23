import json

class Logger():
    def __init__(self):
        self._data = []

    def log_start_pid(self, function, pid, speed = None, duration = None):
        # self._data.append({
        #     'log_type' : 'start',
        #     'function' : function,
        #     'kp' : pid.kp,
        #     'ki' : pid.ki,
        #     'kd' : pid.kd,
        #     'speed' : speed,
        #     'time' : duration
        # })
        pass

    def log_run_pid(self, function, target_angle, actual_angle, correction): 
        # self._data.append({
        #     'log_type' : 'run',
        #     'function' : function,
        #     'target' : target_angle,
        #     'actual' : actual_angle,
        #     'correction' : correction
        # })
        pass


    def stop_pid(self):
        # self._data.append({
        #     'log_type' : 'stop'
        # })
        pass

    def write(self):
        # with open('pid_values.json', 'a') as outfile:
        #     for record in self._data:
        #         json.dump(record, outfile)
        # self._data = [] 
        pass
        


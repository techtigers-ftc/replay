from techtigers import Robot, Pid, LineSensor, LineEdge, Color

from spike import MotorPair, ColorSensor, StatusLight, MotionSensor, Speaker, PrimeHub, Motor
from spike.control import wait_for_seconds

import gc

print("Free memory 1: {}".format(gc.mem_free()))
gc.collect();
print("Free memory 2: {}".format(gc.mem_free()))


robot = Robot()
drive_pid = Pid(10, 0, 2)
reverse_drive_fast = Pid(-3, 0, -9)
reverse_drive_slow = Pid(-10, 0, -5)
turn_pid = Pid(20, 0, 3)

line_follow_pid = Pid(5,0,0)

robot.run_left_attachment(20,5)

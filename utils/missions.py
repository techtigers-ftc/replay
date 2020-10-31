from techtigers import Robot, Pid, LineSensor, LineEdge, Color

from spike import MotorPair, ColorSensor, StatusLight, MotionSensor, Speaker, PrimeHub, Motor
from spike.control import wait_for_seconds

robot = Robot()
drive_pid = Pid(10, 0, 2)
reverse_drive_pid = Pid(-20, 1, 5)
turn_pid = Pid(20, 0, 3)

line_follow_pid = Pid(5,0,0)
robot.reset_gyro()

def ms1():
    robot.run_left_attachment(20,5)

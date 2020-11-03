from techtigers import Robot, Pid, LineSensor, LineEdge, Color

robot = Robot()
drive_pid = Pid(10, 0, 2)
reverse_drive_pid = Pid(-20, 1, 5)
turn_pid = Pid(20, 0, 3)

line_follow_pid = Pid(5,0,0)
robot.reset_gyro()

def ms1():
    robot.run_left_attachment(80,5)
    robot.run_right_attachment(80,5)

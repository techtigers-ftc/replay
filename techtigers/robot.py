from spike import MotorPair, ColorSensor, StatusLight, MotionSensor, Speaker, PrimeHub, Motor
from spike.control import wait_for_seconds
from .colors import Color
from .pid import Pid
from .line_sensor import LineSensor
from .line_edge import LineEdge
from .logger import Logger
from .timer import Timer

class Robot:
    """ Represents the robot for the the 2021 fll season
    """

    def __init__(self):
        """ Initializes the robot's motors and sensors
        """
        self.drive_motors = MotorPair('B', 'D')
        self.left_motor = Motor("B")
        self.right_motor = Motor("D")
        self.left_color = ColorSensor('A')
        self.right_color = ColorSensor('F')
        self.left_attachment = Motor('C')
        self.right_attachment = Motor('E')
        self.hub = PrimeHub()
        self.gyro = self.hub.motion_sensor

        self._logger = Logger()

    def _run_motor(motor, speed, duration):
        """ Hidden function that is used to move single motors

        :param speed: The speed of the motor
        :type speed: Number :param duration: The Amount of time the robot runs for :type duration: Number """
        motor.run_for_seconds(duration, speed)
    def stop_on_color(self, speed, sensor, color=Color.WHITE):
        """This function implements the ability to go at a certain speed
        and then stop on a certain color

            :param speed: The speed at which the robot goes
            :type speed: Number
            :param sensor: Identifies the sensor to stop on a color
            :type sensor: Enumeration
            :param color: Color that the robot will stop on. Defaults to Color.WHITE.
            :type color: Enumeration
        """
        color_sensor =  self.left_color
        if sensor == LineSensor.RIGHT:
            color_sensor = self.right_color

        wait_for_seconds(0.01)
        self.drive_motors.start(0,speed)
        wait = True
        while wait:
            sensor_value = color_sensor.get_reflected_light() 
            wait = sensor_value < color[0] or sensor_value >= color[1]
            pass
        self.drive_motors.stop()

    def drift_check_base(self):
        """ This function checks the gyro value, waits 2 seconds, and checks the value
            again to see if the gyro is drifting.

            :return drift: Checks drift
            :type drift: Boolean
        """
        drift = False
        start_gyro = self.gyro.get_yaw_angle()
        self.hub.status_light.on('blue')
        wait_for_seconds(2)
        if start_gyro != self.gyro.get_yaw_angle():
            self.hub.speaker.beep(80, .2)
            wait_for_seconds(0.1)
            self.hub.speaker.beep(82, .2)
            wait_for_seconds(0.1)
            self.hub.speaker.beep(84, .2)
            wait_for_seconds(0.1)
            self.hub.speaker.beep(85, .2)

            self.hub.status_light.on('red')
            drift = True

        return drift

    def drift_check(self):
        """ This function takes the output of drift_check_base and alerts the user of no
            gyro drift by beeping and changing color
        """
        while self.drift_check_base():
            wait_for_seconds(1)
        self.hub.speaker.beep(50, 1)
        self.hub.status_light.on('green')




    def turn(self, pid, target_angle, tolerance = 1):
        """Turns the robot to a specific angle.

            j:param pid: Uses Pid instance with parameters set beforehand
            :type pid: Class Object
            :param target_angle: Angle the robot turns to
            :type target_angle: Number
            :param tolerance: How close to the target angle you want the robot to be
            :type tolerence: Number
        """
        pid.reset()
        while True:
            actual_angle = self.gyro.get_yaw_angle()
            error = target_angle - actual_angle
            error = error -360*int(error/180)

            steering = pid.compute_steering(error)

            if steering != 0:
                abs_steering = abs(steering)
                sign = steering/abs_steering
                speed = min(10, abs_steering) * sign

            self.left_motor.start(int(speed))
            self.right_motor.start(int(speed))

            if abs(error) < tolerance:
                break

        self.left_motor.stop()
        self.right_motor.stop()

    def reset_gyro(self):
        """ This function resets the gyro value to 0
        """
        self.hub.motion_sensor.reset_yaw_angle()

    def dead_reckon_drive(self, speed, time):
        """ This function drives the motors using tank steering

            :param speed: The speed the motors drive at
            :type speed: Number
            :param time: The amount of seconds the motors drive for
            :type time: Number
        """
        self.drive_motors.move_tank(time,"seconds",speed,speed)

    def follow_line(self, pid, speed, duration, which_sensor, which_edge):
        """Follows the line using a color sensor.

        :param pid: Uses Pid instance with parameters set beforehand
        :type pid: Pid
        :param speed: Speed of the Robot
        :type speed: Number
        :param duration: Duration of the function
        :type duration: Number
        :param which_sensor: The sensor the robot uses to follow the line
        :type which_sensor: LineSensor
        :param which_edge: Which side the white is on relative to the robot
        :type which_edge: LineEdge
        """

        # Inititialize values
        pid.reset()
        clock = Timer()

        duration = duration * 1000000
        while clock.duration() < duration:
            # Selecting which sensor to use using an Enum
            if which_sensor == LineSensor.RIGHT:
                error = 66 - self.right_color.get_reflected_light()
            if which_sensor == LineSensor.LEFT:
                error = 66 - self.left_color.get_reflected_light()

            # Selecting which edge of the line to use
            if which_edge == LineEdge.LEFT:
                pass
            else:
                error = error * -1

            # Calculate steering
            steering = int((pid.compute_steering(error) + 50) / 3.4)
            

            # Run motors
            self.drive_motors.start(steering, speed)

        self.drive_motors.stop()
        # --- TEMP CODE START ---
        print("------")
        print(pid._error_change_min, pid._error_change_max, pid._error_change_total)
        print(pid._total_error_min, pid._total_error_max, pid._total_error_total)
        print(pid._iterations)
        print("------")
        # --- TEMP CODE END ---

    def align(self, speed):
        """Aligns using color sensors on black line

        :param speed: The speed the robot moves at
        :type speed: Number
        """
        self.left_motor.start(-speed)
        self.right_motor.start(speed)
        while True:
            left = False
            right = False
            if self.left_color.get_reflected_light() <= 40:
                self.left_motor.stop()
                left = True
            if self.right_color.get_reflected_light() <= 40:
                self.right_motor.stop()
                right = True
            if left and right == True:
                break
            

    def drive(self, pid, speed, target_angle, duration):
        """
        Gyro drive allows the robot to accurately drive in any direction

        :param pid: Uses Pid instance with parameters set beforehand
        :type pid: Instance of a Class
        :param speed: The speed of the motor
        :type speed: Number
        :param target_angle: The orientation of the robot
        :type target_angle: Number
        :param duration: The Amount of time the robot runs for
        :type duration: Number
        """
        pid.reset()
        clock = Timer()

        duration = duration * 1000000
        while clock.duration() < duration:
            actual_angle = self.gyro.get_yaw_angle()
            error = target_angle - actual_angle
            error = error - 360*int(error/180)

            steering = pid.compute_steering(error)

            self.drive_motors.start(-1 * steering, speed)

        self.drive_motors.stop()

    def run_left_drive(self, speed, duration):
        """Runs the left drive motor for desired speed and time

        :param speed: The speed of the motor
        :type speed: Number
        :param duration: The Amount of time the robot runs for
        :type duration: Number
        """
        Robot._run_motor(self.left_motor, speed, duration)

    def run_right_drive(self, speed, duration):
        """Runs the right drive motor for desired speed and time

        :param speed: The speed of the motor
        :type speed: Number
        :param duration: The Amount of time the robot runs for
        :type duration: Number
        """
        Robot._run_motor(self.right_motor, speed, duration)

    def run_left_attachment(self, speed, duration):
        """Runs the left attachment motor for desired speed and time

        :param speed: The speed of the motor
        :type speed: Number
        :param duration: The Amount of time the robot runs for
        :type duration: Number
        """
        Robot._run_motor(self.left_attachment, speed, duration)

    def run_right_attachment(self, speed, duration):
        """Runs the right attachment motor for desired speed and time

        :param speed: The speed of the motor
        :type speed: Number
        :param duration: The Amount of time the robot runs for
        :type duration: Number
        """
        Robot._run_motor(self.right_attachment, speed, duration)

    def beep(self, note, time):
        """Runs a beep on the spike prime for a certain pitch and time

        :param note: The midi note number from 44 - 123
        :type note: Number
        :param time: The number of seconds the note plays for
        :type time: Number
        """
        self.hub.speaker.beep(note, time)

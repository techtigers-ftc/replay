from spike import MotorPair, ColorSensor, StatusLight, MotionSensor, Speaker, PrimeHub, Motor
from spike.control import wait_for_seconds
from .colors import Color
from .line_sensor import LineSensor
from .line_edge import LineEdge

class Robot:
    """ Represents the robot for the the 2021 fll season
    """

    def __init__(self):
        """ Initializes the robot's motors and sensors
        """
        self.drive_motors = MotorPair('D', 'E')
        self.left_color = ColorSensor('F')
        self.right_color = ColorSensor('C')
        self.hub = PrimeHub()
        self.gyro = self.hub.motion_sensor
        self.left_motor = Motor("D")
        self.right_motor = Motor("E")
        self.LEFT_MOTOR_CONSTANT = -1
        self.RIGHT_MOTOR_CONSTANT = 1

    def stop_on_color(self, speed, sensor, color=Color.WHITE):
        """This function implements the ability to go at a certain speed 
        and then stop on a certain color

        Args:
            speed(number): The speed at which the robot goes
            sensor(LineSensor): Identifies the sensor to stop on a color
            color(Color, optional): Color that the robot will stop on. Defaults to Color.WHITE.
        """
        color_sensor =  self.left_color
        if sensor == LineSensor.RIGHT:
            color_sensor = self.right_color

        self.drive_motors.start(0,speed)
        color_sensor.wait_until_color(color)
        self.drive_motors.stop()

    def drift_check_base(self):
        """ This function checks the gyro value, waits 2 seconds, and checks the value 
            again to see if the gyro is drifting.

        Return:
            drift(boolean): Checks drift
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

        


    def gyro_turn(self, pid, target_angle, tolerance = 1):
        """Turns the robot to a specific angle.

        Args:
            pid(class): Uses Pid instance with parameters set beforehand
            target_angle(number): Angle the robot turns to
            tolerance(number): How close to the target angle you want the robot to be
        """
        pid.reset()
    
        while True:
            actual_angle = self.gyro.get_yaw_angle()
            error = target_angle - actual_angle

            steering = pid.compute_steering(error)

            if steering != 0:
                abs_steering = abs(steering)
                sign = steering/abs_steering
                speed = min(10, abs_steering) * sign
            
            self.left_motor.start(speed * self.LEFT_MOTOR_CONSTANT)
            self.right_motor.start(speed * self.RIGHT_MOTOR_CONSTANT * -1)

            if abs(error) < tolerance:
                break

        self.left_motor.stop()
        self.right_motor.stop()
    
    def reset_gyro(self):
        """ This function resets the gyro value to 0
        """
        hub = PrimeHub()
        hub.motion_sensor.reset_yaw_angle()
    
    def dead_reckon_drive(self, speed, time):
        """ This function drives the motors using tank steering
        
        Args:
            speed(number): The speed the motors drive at
            time(number): The amount of seconds the motors drive for
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

        while pid.clock.now() < duration:
            # Selecting which sensor to use using an Enum
            if which_sensor == LineSensor.RIGHT:
                error = 50 - self.right_color.get_reflected_light()
            if which_sensor == LineSensor.LEFT:
                error = 50 - self.left_color.get_reflected_light()

            # Selecting which edge of the line to use
            if which_edge == LineEdge.RIGHT:
                pass
            else:
                error = error * -1

            # Calculate steering
            steering = pid.compute_steering(error)

            # Run motors
            self.drive_motors.start(steering, speed)

        self.drive_motors.stop()
    
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
            if self.left_color.get_reflected_light() <= 10:
                self.left_motor.stop()
                left = True
            if self.right_color.get_reflected_light() <= 10:
                self.right_motor.stop()
                right = True
            if left and right == True:
                break
            print(self.left_color.get_reflected_light(), self.right_color.get_reflected_light())

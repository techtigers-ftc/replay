from spike import MotorPair, ColorSensor, StatusLight, MotionSensor, Speaker, PrimeHub, Motor
from spike.control import wait_for_seconds
from .colors import Color
from .line_sensor import LineSensor


class Robot:
    """ Represents the robot for the the 2021 fll season
    """

    def __init__(self):
        """ Initializes the robot's motors and sensors
        """
        self.drive_motors = MotorPair('C', 'E')
        self.left_color_sensor = ColorSensor('F')
        self.right_color_sensor = ColorSensor('D')
        self.hub = PrimeHub()
        self.gyro = self.hub.motion_sensor
        self.left_motor = Motor("C")
        self.right_motor = Motor("E")
        self.LEFT_MOTOR_CONSTANT = -1
        self.RIGHT_MOTOR_CONSTANT = 1

    def stop_on_color(self, speed, sensor, color=Color.WHITE):
        """This function implements the ability to go at a certain speed 
        and then stop on a certain color

        Args:
            speed (number): The speed at which the robot goes
            sensor (LineSensor): Identifies the sensor to stop on a color
            color (Color, optional): Color that the robot will stop on. Defaults to Color.WHITE.
        """
        color_sensor =  self.left_color_sensor
        if sensor == LineSensor.RIGHT:
            color_sensor = self.right_color_sensor

        self.drive_motors.start(0,speed)
        color_sensor.wait_until_color(color)
        self.drive_motors.stop()

    def drift_check_base(self):
        """ This function checks the gyro value, waits 2 seconds, and checks the value 
            again to see if the gyro is drifting.

        Return:
            drift (boolean): Checks drift
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
        while self.drift_check_base():
            wait_for_seconds(1)
        self.hub.speaker.beep(50, 1)
        


    def gyro_turn(self, pid, target_angle, tolerance = 1):
        """Turns the robot to a specific angle.
        :param pid: Uses Pid instance with parameters set beforehand
        :type pid: Number
        :param target_angle: Angle the robot turns to
        :type target_angle: Number
        :param tolerance: How close to the target angle you want the robot to be
        :type tolerance: Number
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
                # Pay attention!
            
            self.left_motor.start(int(speed * self.LEFT_MOTOR_CONSTANT))
            self.right_motor.start(int(speed * self.RIGHT_MOTOR_CONSTANT * -1))

            if abs(error) < tolerance:
                break

        self.left_motor.stop()
        self.right_motor.stop()



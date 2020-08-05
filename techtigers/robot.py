from spike import MotorPair, ColorSensor, StatusLight, MotionSensor, Speaker, PrimeHub
from spike.control import wait_for_seconds
from .colors import Color
from .line_sensor import LineSensor
hub = PrimeHub()

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
        self.gyro = 

    def stop_on_color(self, speed, sensor, color=Color.WHITE):
        """This functuion implements the ability to go at a certain speed 
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

    def drift_check(self):
        hub.speaker.beep(60, 0.2)
        wait_for_seconds(0.1)
        hub.speaker.beep(60, 0.2)
        drift = False
        start_gyro = self.gyro.get_yaw_angle()
        hub.status_light.on('blue')

        wait_for_seconds(2)
        
        if start_gyro != self.gyro.get_yaw_angle():
            hub.status_light.on('red')
            drift = True
 
        return drift 
    def gyro_turn(self, pid, target_angle, tolerance = 1):
        """Turns the robot to a specific angle.
        :param pid: Uses Pid instance with parameters set beforehand
        :type pid: Number
        :param target_angle: Angle the robot turns to
        :type target_angle: Number
        :param tolerance: How close to the target angle you want the robot to be
        :type tolerance: Number
        """

        # Inititialize values
        pid.reset()
        
        target_angle = target_angle % 360
        error = tolerance + 1
        min_speed = 50



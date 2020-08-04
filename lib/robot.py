from spike import MotorPair, ColorSensor
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
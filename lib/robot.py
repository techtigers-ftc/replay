from spike import MotorPair, ColorSensor

class Robot:
    """ Represents the robot for the the 2021 fll season
    """

    def __init__(self):
        """ Initializes the robot's motors and sensors
        """

        self.drive_motors = MotorPair('C', 'E')

    def stop_on_color(self ,speed,color="white"):
        """ Drives the robot until it reads white
        """
        motor_pair.start(0,speed)
        color_sensor = ColorSensor('F')
        color_sensor.wait_until_color(color)
        motor_pair.stop()

        



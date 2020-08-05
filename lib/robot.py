from spike import MotorPair, ColorSensor

class Robot:
    """ Represents the robot for the the 2021 fll season
    """

    def __init__(self):
        """ Initializes the robot's motors and sensors
        """

        self.drive_motors = MotorPair('C', 'E')
        self.gyro = hub.motion_sensor

    def stop_on_color(self ,speed,color="white"):
        """ Drives the robot until it reads white
        """
        motor_pair.start(0,speed)
        color_sensor = ColorSensor('F')
        color_sensor.wait_until_color(color)
        motor_pair.stop()

    def drift_check(self):
        hub.speaker.beep(60, 0.2)
        wait_for_seconds(0.1)
        hub.speaker.beep(60, 0.2)
        drift = False
        start_gyro = self.gyro.get_yaw_angle()
        hub.status_light.on('blue')

        wait_for_seconds(2)
        
        if start_gyro != self.gyro.get_yaw_angle()
            hub.status_light.on('red')
            drift = True
 
        return drift 



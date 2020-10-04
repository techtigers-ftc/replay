
class ColorMatcher:
    def __init__(self, color_value):
        """ ColorMatcher takes the sensor value and converts it into a color

        :param color_value: The color based on the color_sensor value
        """
        self._color_value = color_value


    def is_match(self, color_sensor):
        """
        :param color_sensor:The reflected light intensisty of the color sensor 
        """
        sensor_value = color_sensor.get_color() 
        return sensor_value == self._color_value

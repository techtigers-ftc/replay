class ReflectedLightMatcher:
    def __init__(self, min_value, max_value):
        """The ReflectedLightMatcher takes the value from the color_sensor and
        checks to see if it fits in the min/max values of different colors

        :param min_value: The minimium reflected_sensor value of a given color
        :param max_value: The maximum reflected_senor value of a given color
        """
        self._min_value = min_value
        self._max_value = max_value


    def is_match(self, color_sensor):
        """
        :param color_sensor: The reflected light from the color_sesnor 
        """
        sensor_value = color_sensor.get_reflected_light() 
        return sensor_value > self._min_value and sensor_value <= self._max_value

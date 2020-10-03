class ReflectedLightMatcher:
    def __init__(self, min_value, max_value):
        self._min_value = min_value
        self._max_value = max_value


    def is_match(self, color_sensor):
        sensor_value = color_sensor.get_reflected_light() 
        return sensor_value > self._min_value and sensor_value <= self._max_value


class ColorMatcher:
    def __init__(self, color_value):
        self._color_value = color_value


    def is_match(self, color_sensor):
        sensor_value = color_sensor.get_color() 
        return sensor_value == self._color_value

class Color:
    """Enumeration of supported "stop on" colors
    """

    """White color
    """
    # WHITE = (100, 101)
    WHITE = ColorMatcher('white')

    """Black color
    """
    BLACK = ReflectedLightMatcher(0, 35)

    """Green color
    """
    GREEN = ReflectedLightMatcher(80, 91)



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


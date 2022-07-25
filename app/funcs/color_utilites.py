
from colour import Color

def color_variant(hex_color, saturation=0.3):
    """ takes a color like #87c95f and produces a lighter or darker variant """
    if len(hex_color) != 7:
        raise Exception(
            "Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    c = Color(hex_color)
    c.saturation = saturation
    return c.hex_l
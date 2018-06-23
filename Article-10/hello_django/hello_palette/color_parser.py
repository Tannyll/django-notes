import operator
import colorific
from PIL import Image


class ColorParser(object):
    def __init__(self, image_path):
        self.image = Image.open(image_path)

    def parse_colors(self):
        palette = colorific.extract_colors(self.image)
        palette_dict = {}
        for color in palette.colors:
            color_hex = colorific.rgb_to_hex(color.value)
            palette_dict[color_hex] = color.prominence
        colors = sorted(palette_dict.items(), key=operator.itemgetter(1), reverse=True)
        return ','.join([c[0] for c in colors])

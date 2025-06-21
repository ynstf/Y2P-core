class Colors:
    dark_grey = (21, 21, 30)
    green = (61, 179, 93)
    red = (237, 90, 90)
    orange = (255, 147, 61)
    yellow = (255, 217, 61)
    purple = (173, 84, 198)
    cyan = (55, 214, 227)
    blue = (63, 111, 245)
    white = (255, 255, 255)
    dark_blue = (44, 44, 127)
    light_blue = (59, 85, 162)

    @classmethod
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]
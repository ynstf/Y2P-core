class Colors:
    dark_grey = (21, 21, 21)
    green = (44, 189, 85)
    red = (189, 66, 44)
    orange = (194, 128, 44)
    yellow = (243, 219, 64)
    purple = (164, 51, 198)
    cyan = (64, 227, 222)
    blue = (44, 135, 192)
    white = (255, 255, 255)
    dark_blue = (44, 44, 127)
    light_blue = (59, 85, 162)

    @classmethod
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]
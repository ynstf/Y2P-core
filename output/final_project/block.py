import pygame
from colors import Colors
from position import Position

class Block():
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.rotation_state = 0
        self.row_offset = 0
        self.column_offset = 0
        self.color = Colors.get_cell_colors()

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        moved_tiles = []
        tiles = self.cells[self.rotation_state]
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles
    
    def rotate(self):
        self.rotation_state += 1
        if  self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        self.rotation_state -= 1
        if  self.rotation_state == 0:
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen, offset_x, offset_y):
        tiles = self.cells[self.rotation_state]
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column * self.cell_size, offset_y + tile.row * self.cell_size , self.cell_size - 0, self.cell_size -0)
            pygame.draw.rect(screen, self.color[self.id], tile_rect, 0,0)
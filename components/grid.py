import pygame
from components.spot import Spot

GREY = (128, 128, 128)
WHITE = (255, 255, 255)

class Grid:
    def __init__(self, win, rows, width):
        gap = width // rows
        grid = [[Spot(i, j, gap, rows) for j in range(rows)] for i in range(rows)]

        self.rows = rows
        self.width = width
        self.grid = grid
        self.win = win

    def _draw_grid(self):
        """
        Draws grid lines

        Returns:
        - None
        """
        gap = self.width // self.rows
        for i in range(self.rows):
            pygame.draw.line(self.win, GREY, (0, i * gap), (self.width, i * gap))
            pygame.draw.line(self.win, GREY, (i * gap, 0), (i * gap, self.width))

    def draw(self):
        """
        Draw/update the surface based on changes to grid

        Returns:
        - None
        """
        self.win.fill(WHITE)

        for row in self.grid:
            for spot in row:
                spot.draw(self.win)

        self._draw_grid()
        pygame.display.update()

    def update_neighbours(self):
        for row in self.grid:
            for spot in row:
                spot.update_neighbors(self.grid)
    
    def get_spot(self, row, col):
        return self.grid[row][col]

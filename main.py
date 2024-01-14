import pygame
import time

from algorithms import dijkstra, a_star, bellman_ford
from components.grid import Grid
from components.spot import Spot


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


def get_clicked_pos(pos, rows, width):
    """
    Get the coordinates of the clicked box

    Returns:
    - tuple: (row, column)
    """
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap

    return row, col


def main(win, width, rows):
    algorithm_name = "No Algorithm Previously Run"
    traverse_time = 0
    traversed_nodes = 0
    path_length = 0

    start = None
    end = None
    running = True

    algorithm = dijkstra
    G = Grid(win, rows, width)  # init grid
    while running:
        G.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # Left click - Set start/stop/barrier
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = G.get_spot(row, col)
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif end and start and spot != start and spot != end:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right click - Delete block
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = G.get_spot(row, col)
                if spot.is_end():
                    end = None
                if spot.is_start():
                    start = None
                spot.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:  # Spacebar - Run Algo
                    G.update_neighbours()
                    for row in G.grid:
                        for spot in row:
                            spot.update_neighbors(G.grid)
                            if spot.is_open() or spot.is_closed() or spot.is_path():
                                spot.reset()

                    # Run algorithm
                    algorithm_name, traverse_time, traversed_nodes,  path_length = algorithm.run(lambda: G.draw(), G.grid, start, end)
        
                if event.key == pygame.K_s: # S - Switch algorithm
                    if algorithm == dijkstra:
                        algorithm = a_star
                        algorithm_name = "A* Algorithm"
                    elif algorithm == a_star:
                        algorithm = bellman_ford
                        algorithm_name = "Bellman-Ford Algorithm"
                    else:
                        algorithm = dijkstra
                        algorithm_name = "Dijkstra's Algorithm"

                    # Display algorithm name
                    win.blit(pygame.font.SysFont('Arial', 20).render(algorithm_name, True, (0, 0, 0), (220, 220, 220)), (0, 0))
                    pygame.display.update()
                    time.sleep(1.3)
                    win.blit(pygame.font.SysFont('Arial', 20).render(algorithm_name, True, (255, 255, 255)), (0, 0))
                    pygame.display.update()

                if event.key == pygame.K_c: # C - Reset start and end point
                    start = None
                    end = None
                    for row in G.grid:
                        for spot in row:
                            if not spot.is_barrier():
                                spot.reset()

                if event.key == pygame.K_r: # R - Reset whole board
                    start = None
                    end = None
                    for row in G.grid:
                        for spot in row:
                            spot.reset()

                if event.key == pygame.K_i: # I - Display statistics 
                    win.blit(pygame.font.SysFont('Arial', 20).render(algorithm_name, True, (0, 0, 0), (220, 220, 220)), (0, 0))
                    win.blit(pygame.font.SysFont('Arial', 20).render("Traverse time: " + str(traverse_time), True, (0, 0, 0), (220, 220, 220)), (0, 25))
                    win.blit(pygame.font.SysFont('Arial', 20).render("Traversed nodes: " + str(traversed_nodes), True, (0, 0, 0), (220, 220, 220)), (0, 50))
                    win.blit(pygame.font.SysFont('Arial', 20).render("Path length: " + str(path_length), True, (0, 0, 0), (220, 220, 220)), (0, 75))
                    pygame.display.update()

                    # Press any key to close the statistics
                    waiting_for_key = True
                    while waiting_for_key:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                waiting_for_key = False
                                win.fill(WHITE, (0, 0, 300, 80))
                                pygame.display.update()
                            if event.type == pygame.QUIT:
                                pygame.quit()

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    WIDTH = 800
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    ROWS = 50
    main(WIN, WIDTH, ROWS)

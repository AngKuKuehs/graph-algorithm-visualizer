from dijkstar import Graph, find_path
from algorithms.dijkstra import run
from components.grid import Grid
from components.spot import Spot
import time

def find_grid_path(start: Spot):
    res = []
    visited = set()
    brk = True
    curr = start
    while brk:
        brk = False
        visited.add(curr)
        res.append((curr.row, curr.col))
        for adj in curr.neighbors:
            if adj.is_path() and adj not in visited:
                brk = True
                curr = adj
                break
            if adj.is_end():
                res.append((adj.row, adj.col))
                return res
    return []

def test_compare_algorithms():
    beaten = 0
    rows = 400
    grid = Grid(None, rows, 1)

    start = grid.grid[0][0]
    end = grid.grid[0][rows-1]
    start.make_start()
    end.make_end()

    # horizontal barriers
    # for i in range(1, rows):
    #     grid.grid[1][i].make_barrier()

    # diagonal barriers
    for i in range(rows):
        grid.grid[i][i].make_barrier()

    # vertical barriers
    # for i in range(1, rows):
    #     grid.grid[i][0].make_barrier()
    #     grid.grid[i][rows-1].make_barrier()


    for _ in range(100):

        # Own algorithm
        grid.update_neighbours()
        _, own_time, _, _ = run(lambda: None, grid.grid, start, end)

        ## Inbuilt
        graph = Graph()
        for row in grid.grid:
            for spot in row:
                if not spot.is_barrier():
                    for adj in spot.neighbors:
                        graph.add_edge(u=spot, v=adj, edge=1)
        inbuilt_start_time = time.time()
        find_path(graph, start, end)
        inbuilt_time = time.time() - inbuilt_start_time

        if own_time < inbuilt_time:
            beaten += 1

    # Compare time:
    print(beaten)
    assert beaten > 50


test_compare_algorithms()
